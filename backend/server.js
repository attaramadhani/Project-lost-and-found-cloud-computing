const express = require('express');
const cors = require('cors');
const os = require('os');
const dotenv = require('dotenv');
const db = require('./db');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const INSTANCE_NAME = process.env.APP_INSTANCE || `backend-${os.hostname()}`;

// Middleware
app.use(cors());
app.use(express.json());

// Cloud Computing Metadata Middleware: inject X-Served-By header in every response
app.use((req, res, next) => {
  res.setHeader('X-Served-By', INSTANCE_NAME);
  res.setHeader('X-Hostname', os.hostname());
  next();
});

// Root Endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Campus Lost & Found REST API',
    course: 'Cloud Computing',
    served_by: INSTANCE_NAME,
    hostname: os.hostname(),
    uptime: process.uptime()
  });
});

// Health Check Endpoint (Used by Load Balancer and Demo verification)
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    served_by: INSTANCE_NAME,
    hostname: os.hostname(),
    database: db.getDatabaseStatus(),
    memory_usage_mb: Math.round(process.memoryUsage().rss / 1024 / 1024)
  });
});

// Get All Items (with filter & search)
app.get('/api/items', async (req, res) => {
  try {
    const { type, status, search, category } = req.query;
    const items = await db.getAllItems({ type, status, search, category });
    res.json({
      success: true,
      total: items.length,
      served_by: INSTANCE_NAME,
      data: items
    });
  } catch (err) {
    console.error('Error fetching items:', err);
    res.status(500).json({ success: false, error: 'Internal Server Error', served_by: INSTANCE_NAME });
  }
});

// Get Item by ID
app.get('/api/items/:id', async (req, res) => {
  try {
    const item = await db.getItemById(req.params.id);
    if (!item) {
      return res.status(404).json({ success: false, message: 'Item not found', served_by: INSTANCE_NAME });
    }
    res.json({ success: true, served_by: INSTANCE_NAME, data: item });
  } catch (err) {
    console.error('Error fetching item:', err);
    res.status(500).json({ success: false, error: 'Internal Server Error', served_by: INSTANCE_NAME });
  }
});

// Create New Item
app.post('/api/items', async (req, res) => {
  try {
    const { title, type, category, description, location, date_event, contact_name, contact_phone } = req.body;

    if (!title || !type || !description || !location || !contact_name || !contact_phone) {
      return res.status(400).json({
        success: false,
        message: 'Lengkapi semua field yang diperlukan (title, type, description, location, contact_name, contact_phone)'
      });
    }

    const createdItem = await db.createItem({
      title,
      type,
      category: category || 'Lain-lain',
      description,
      location,
      date_event: date_event || new Date().toISOString().split('T')[0],
      contact_name,
      contact_phone
    });

    res.status(201).json({
      success: true,
      message: 'Laporan berhasil dibuat',
      served_by: INSTANCE_NAME,
      data: createdItem
    });
  } catch (err) {
    console.error('Error creating item:', err);
    res.status(500).json({ success: false, error: 'Internal Server Error', served_by: INSTANCE_NAME });
  }
});

// Update Status (e.g. resolve)
app.patch('/api/items/:id/status', async (req, res) => {
  try {
    const { status } = req.body;
    if (!['open', 'resolved'].includes(status)) {
      return res.status(400).json({ success: false, message: 'Status must be open or resolved' });
    }

    const updated = await db.updateItemStatus(req.params.id, status);
    if (!updated) {
      return res.status(404).json({ success: false, message: 'Item not found' });
    }

    res.json({
      success: true,
      message: `Status berhasil diubah menjadi ${status}`,
      served_by: INSTANCE_NAME,
      data: updated
    });
  } catch (err) {
    console.error('Error updating status:', err);
    res.status(500).json({ success: false, error: 'Internal Server Error' });
  }
});

// Delete Item
app.delete('/api/items/:id', async (req, res) => {
  try {
    const success = await db.deleteItem(req.params.id);
    if (!success) {
      return res.status(404).json({ success: false, message: 'Item not found' });
    }
    res.json({
      success: true,
      message: 'Laporan berhasil dihapus',
      served_by: INSTANCE_NAME
    });
  } catch (err) {
    console.error('Error deleting item:', err);
    res.status(500).json({ success: false, error: 'Internal Server Error' });
  }
});

// Start server
async function start() {
  await db.initDatabase();
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`====================================================`);
    console.log(`🚀 [Cloud Backend] Server running on port ${PORT}`);
    console.log(`🏷️  [Instance Name] ${INSTANCE_NAME}`);
    console.log(`💻 [Host Machine]  ${os.hostname()}`);
    console.log(`🔗 [API Health]    http://localhost:${PORT}/api/health`);
    console.log(`📋 [API Items]     http://localhost:${PORT}/api/items`);
    console.log(`====================================================`);
  });
}

start();
