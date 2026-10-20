const mysql = require('mysql2/promise');
const dotenv = require('dotenv');
dotenv.config();

let pool = null;
let useFallback = false;

// In-Memory fallback store for seamless local testing without running MySQL
let inMemoryItems = [
  {
    id: 1,
    title: 'KTM Universitas Trunojoyo Madura An. Dimas Prasetyo',
    type: 'lost',
    category: 'Dokumen/KTM',
    description: 'KTM hilang bersama dompet coklat kulit. Ada stiker hologram UTM.',
    location: 'Gedung RKB Lt 2',
    date_event: '2026-10-07',
    contact_name: 'Dimas Prasetyo',
    contact_phone: '081234567890',
    status: 'open',
    created_at: new Date('2026-10-07T08:30:00Z'),
    updated_at: new Date('2026-10-07T08:30:00Z')
  },
  {
    id: 2,
    title: 'Kunci Motor Honda Vario dengan Gantungan Karakter Doraemon',
    type: 'found',
    category: 'Kendaraan/Kunci',
    description: 'Ditemukan tergantung di stop kontak gazebo dekat perpustakaan pusat.',
    location: 'Gazebo Depan Perpustakaan',
    date_event: '2026-10-08',
    contact_name: 'Siti Rahma',
    contact_phone: '082198765432',
    status: 'open',
    created_at: new Date('2026-10-08T09:15:00Z'),
    updated_at: new Date('2026-10-08T09:15:00Z')
  },
  {
    id: 3,
    title: 'Earphone Bluetooth TWS Hitam Baseus',
    type: 'found',
    category: 'Elektronik',
    description: 'Tertinggal di meja paling belakang Lab Komputer C.',
    location: 'Lab Komputer C',
    date_event: '2026-10-08',
    contact_name: 'Laboran Lab',
    contact_phone: '085712345678',
    status: 'open',
    created_at: new Date('2026-10-08T11:00:00Z'),
    updated_at: new Date('2026-10-08T11:00:00Z')
  },
  {
    id: 4,
    title: 'Jaket Hoodie Abu-abu Kampus SI UTM',
    type: 'lost',
    category: 'Pakaian/Aksesoris',
    description: 'Lupa ditaruh di kursi kantin teknik saat jam istirahat siang.',
    location: 'Kantin Fakultas Teknik',
    date_event: '2026-10-06',
    contact_name: 'Rian Hidayat',
    contact_phone: '081345678912',
    status: 'resolved',
    created_at: new Date('2026-10-06T13:45:00Z'),
    updated_at: new Date('2026-10-07T10:00:00Z')
  }
];
let nextId = 5;

async function initDatabase() {
  const host = process.env.DB_HOST || 'localhost';
  const user = process.env.DB_USER || 'root';
  const password = process.env.DB_PASSWORD || '';
  const database = process.env.DB_NAME || 'lost_found_db';
  const port = parseInt(process.env.DB_PORT || '3306', 10);

  try {
    pool = mysql.createPool({
      host,
      user,
      password,
      database,
      port,
      waitForConnections: true,
      connectionLimit: 10,
      queueLimit: 0,
      connectTimeout: 3000
    });

    // Test connection
    const conn = await pool.getConnection();
    console.log(`[DB] Connected successfully to MySQL at ${host}:${port}/${database}`);

    // Create table if not exists automatically
    await conn.query(`
      CREATE TABLE IF NOT EXISTS \`items\` (
        \`id\` INT AUTO_INCREMENT PRIMARY KEY,
        \`title\` VARCHAR(150) NOT NULL,
        \`type\` ENUM('lost', 'found') NOT NULL,
        \`category\` VARCHAR(50) NOT NULL,
        \`description\` TEXT NOT NULL,
        \`location\` VARCHAR(150) NOT NULL,
        \`date_event\` DATE NOT NULL,
        \`contact_name\` VARCHAR(100) NOT NULL,
        \`contact_phone\` VARCHAR(25) NOT NULL,
        \`status\` ENUM('open', 'resolved') NOT NULL DEFAULT 'open',
        \`created_at\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        \`updated_at\` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    `);

    // Check if table is empty, seed initial data
    const [rows] = await conn.query('SELECT COUNT(*) as cnt FROM items');
    if (rows[0].cnt === 0) {
      console.log('[DB] Seeding initial data to MySQL...');
      for (const item of inMemoryItems) {
        await conn.query(
          `INSERT INTO items (title, type, category, description, location, date_event, contact_name, contact_phone, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [item.title, item.type, item.category, item.description, item.location, item.date_event, item.contact_name, item.contact_phone, item.status]
        );
      }
    }

    conn.release();
    useFallback = false;
  } catch (err) {
    console.warn(`[DB] Notice: MySQL not accessible (${err.message}).`);
    console.warn('[DB] Operating in in-memory mode for local development/testing.');
    console.warn('[DB] In production (VM 3 Docker MySQL), it will connect via DB_HOST in .env.');
    useFallback = true;
  }
}

// Data Access Layer
async function getAllItems({ type, status, search, category }) {
  if (useFallback) {
    let result = [...inMemoryItems];
    if (type) result = result.filter(i => i.type === type);
    if (status) result = result.filter(i => i.status === status);
    if (category) result = result.filter(i => i.category.toLowerCase() === category.toLowerCase());
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(i => 
        i.title.toLowerCase().includes(q) || 
        i.description.toLowerCase().includes(q) || 
        i.location.toLowerCase().includes(q)
      );
    }
    return result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  let sql = 'SELECT * FROM items WHERE 1=1';
  const params = [];

  if (type) {
    sql += ' AND type = ?';
    params.push(type);
  }
  if (status) {
    sql += ' AND status = ?';
    params.push(status);
  }
  if (category) {
    sql += ' AND category = ?';
    params.push(category);
  }
  if (search) {
    sql += ' AND (title LIKE ? OR description LIKE ? OR location LIKE ?)';
    const q = `%${search}%`;
    params.push(q, q, q);
  }

  sql += ' ORDER BY created_at DESC';
  const [rows] = await pool.query(sql, params);
  return rows;
}

async function getItemById(id) {
  if (useFallback) {
    return inMemoryItems.find(i => i.id === parseInt(id, 10)) || null;
  }
  const [rows] = await pool.query('SELECT * FROM items WHERE id = ?', [id]);
  return rows[0] || null;
}

async function createItem(data) {
  const { title, type, category, description, location, date_event, contact_name, contact_phone } = data;
  
  if (useFallback) {
    const newItem = {
      id: nextId++,
      title,
      type,
      category,
      description,
      location,
      date_event,
      contact_name,
      contact_phone,
      status: 'open',
      created_at: new Date(),
      updated_at: new Date()
    };
    inMemoryItems.unshift(newItem);
    return newItem;
  }

  const [res] = await pool.query(
    `INSERT INTO items (title, type, category, description, location, date_event, contact_name, contact_phone, status) 
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open')`,
    [title, type, category, description, location, date_event, contact_name, contact_phone]
  );
  return getItemById(res.insertId);
}

async function updateItemStatus(id, status) {
  if (useFallback) {
    const item = inMemoryItems.find(i => i.id === parseInt(id, 10));
    if (item) {
      item.status = status;
      item.updated_at = new Date();
    }
    return item || null;
  }

  await pool.query('UPDATE items SET status = ?, updated_at = NOW() WHERE id = ?', [status, id]);
  return getItemById(id);
}

async function deleteItem(id) {
  if (useFallback) {
    const idx = inMemoryItems.findIndex(i => i.id === parseInt(id, 10));
    if (idx !== -1) {
      inMemoryItems.splice(idx, 1);
      return true;
    }
    return false;
  }

  const [res] = await pool.query('DELETE FROM items WHERE id = ?', [id]);
  return res.affectedRows > 0;
}

function getDatabaseStatus() {
  return {
    mode: useFallback ? 'in-memory-fallback' : 'mysql-connected',
    host: process.env.DB_HOST || 'localhost',
    database: process.env.DB_NAME || 'lost_found_db'
  };
}

module.exports = {
  initDatabase,
  getAllItems,
  getItemById,
  createItem,
  updateItemStatus,
  deleteItem,
  getDatabaseStatus
};
