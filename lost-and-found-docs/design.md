# Desain Sistem & Arsitektur Cloud: Campus Lost & Found (VirtualBox Multi-VM)

Dokumen ini menjelaskan arsitektur sistem, topologi jaringan virtualisasi lokal (Hypervisor Type-2), skema basis data, dan spesifikasi REST API untuk proyek **Campus Lost & Found**.

---

## 1. Arsitektur Virtualisasi & Deployment (Type-2 Hypervisor)

Sistem dirancang mengimplementasikan konsep **Virtualisasi Server & On-Premise Cloud** sesuai materi Pertemuan 02 (Slide 10-11: *Physical Server $\rightarrow$ Hypervisor $\rightarrow$ Virtual Machines*).

Seluruh sistem berjalan di atas laptop fisik (Host) dengan **16 GB RAM** menggunakan **Oracle VM VirtualBox** sebagai Hypervisor:

```
┌────────────────────────────────────────────────────────────────────────┐
│ PHYSICAL HOST: Laptop MSI (Intel Core i7-13620H, 16 GB RAM, Windows 11)│
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ HYPERVISOR (Type-2): Oracle VM VirtualBox                        │  │
│  │ Jaringan Virtual: Host-Only Adapter (Subnet 192.168.56.0/24)     │  │
│  └──────────────────┬─────────────────┬──────────────────┬──────────┘  │
│                     │                 │                  │             │
│                     ▼                 ▼                  ▼             │
│  ┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────┐ │
│  │ VM 1: FRONT-END       │ │ VM 2: BACK-END        │ │ VM 3: DATABASE│ │
│  │ IP: 192.168.56.101    │ │ IP: 192.168.56.102    │ │ IP: .56.103   │ │
│  │ RAM: 1.0 GB           │ │ RAM: 1.5 GB           │ │ RAM: 1.0 GB   │ │
│  │ OS: Ubuntu Server     │ │ OS: Ubuntu Server     │ │ OS: Ubuntu Srv│ │
│  │                       │ │                       │ │               │ │
│  │ Web Server (Nginx)    │ │ Nginx Load Balancer   │ │ Docker MySQL 8│ │
│  │ Serving React SPA     │ │ (Port 80 Round-Robin) │ │ (Port 3306)   │ │
│  │                       │ │         │             │ │               │ │
│  │                       │ │   ┌─────┴─────┐       │ │ Volume:       │ │
│  │                       │ │   ▼           ▼       │ │ /var/lib/mysql│ │
│  │                       │ │ Container 1 Container 2││ (Persistent)  │ │
│  │                       │ │ (Port 5001) (Port 5002│ │               │ │
│  └───────────────────────┘ └───────────┬───────────┘ └───────▲───────┘ │
│                     ▲                  │                     │         │
│                     │                  └────── Query SQL ────┘         │
│                     │ Request API (/api/*)                             │
│                     └──────────────────────────────────────────────────┘
└───────────────────────────────────▲────────────────────────────────────┘
                                    │ Akses Browser: http://192.168.56.101
                      [ Browser Klien di Laptop Host ]
```

---

## 2. Topologi Jaringan & Alokasi IP (Host-Only Network)

Jaringan virtual dikonfigurasi menggunakan mode **Host-Only Adapter (`vboxnet0` / VirtualBox Host-Only Ethernet Adapter)**. Mode ini memungkinkan Host Windows dan seluruh VM saling berkomunikasi secara aman, cepat, dan **100% offline tanpa membutuhkan koneksi internet saat live demo**:

| Node / Mesin | Role | IP Address Virtual | Alokasi Resource | Layanan yang Berjalan |
| :--- | :--- | :--- | :--- | :--- |
| **Host Machine** | Windows 11 (MSI Laptop) | `192.168.56.1` | - | Web Browser (Client) & SSH Terminal |
| **VM 1** | Front-end Server | `192.168.56.101` | 1 vCPU, 1024 MB RAM | Nginx (serving React SPA build) |
| **VM 2** | Back-end Cluster | `192.168.56.102` | 2 vCPU, 1536 MB RAM | Nginx Load Balancer + 2x Container Docker Backend |
| **VM 3** | Database Server | `192.168.56.103` | 1 vCPU, 1024 MB RAM | Container Docker MySQL 8 (Persistent Volume) |

### Aturan Keamanan Jaringan (Firewall / UFW Rules):
1. **VM 1 (Frontend):** Buka port `80` (HTTP) dan port `22` (SSH).
2. **VM 2 (Backend Cluster):** Buka port `80` (Load Balancer Nginx) dan port `22`. Port internal container (`5001` & `5002`) hanya diakses lokal dari balik Nginx.
3. **VM 3 (Database):** Buka port `3306` **khusus hanya untuk IP `192.168.56.102` (VM 2)**. Port database tertutup untuk VM lain dan laptop host.

---

## 3. Skema Basis Data (Database Schema)

Database menggunakan RDBMS MySQL 8 yang berjalan di dalam kontainer Docker di VM 3.

### Tabel `items`
| Kolom | Tipe Data | Keterangan |
| :--- | :--- | :--- |
| `id` | `INT AUTO_INCREMENT PRIMARY KEY` | ID unik laporan barang |
| `title` | `VARCHAR(150) NOT NULL` | Judul barang (misal: "KTM An. Dimas Prasetyo") |
| `type` | `ENUM('lost', 'found') NOT NULL` | Tipe: Hilang (`lost`) atau Ditemukan (`found`) |
| `category` | `VARCHAR(50) NOT NULL` | Kategori barang (Dokumen/KTM, Kendaraan/Kunci, Elektronik, dll.) |
| `description` | `TEXT NOT NULL` | Deskripsi lengkap kronologi & ciri-ciri fisik barang |
| `location` | `VARCHAR(150) NOT NULL` | Lokasi kejadian (misal: "Gazebo Depan Perpustakaan") |
| `date_event` | `DATE NOT NULL` | Tanggal perkiraan kejadian |
| `contact_name` | `VARCHAR(100) NOT NULL` | Nama penemu / pelapor |
| `contact_phone`| `VARCHAR(25) NOT NULL` | Nomor WhatsApp kontak |
| `status` | `ENUM('open', 'resolved') DEFAULT 'open'` | Status: Masih dicari (`open`) / Sudah kembali (`resolved`) |
| `created_at` | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Waktu laporan dibuat |
| `updated_at` | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE` | Waktu laporan diubah |

---

## 4. Spesifikasi REST API & Load Balancing

Setiap response dari backend menyertakan identifier instance (`served_by` dan header `X-Served-By`):

### 1. `GET /api/health`
* **Response Contoh:**
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-10-09T13:00:00Z",
    "served_by": "backend-node-1",
    "hostname": "9b12a8ef31d0",
    "database": {
      "mode": "mysql-connected",
      "host": "192.168.56.103",
      "database": "lost_found_db"
    }
  }
  ```

### 2. `GET /api/items` (Mendukung Query Filter & Pencarian Teks)
* **Query:** `?type=lost|found&status=open|resolved&search=ktm`

### 3. `POST /api/items` (Membuat Laporan Baru)

### 4. `PATCH /api/items/:id/status` (Mengubah Status Kasus Menjadi Resolved)

### 5. `DELETE /api/items/:id` (Menghapus Laporan)
