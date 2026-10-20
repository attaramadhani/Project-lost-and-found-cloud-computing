# Campus Lost & Found - Cloud Computing Project

Proyek Final Mata Kuliah Cloud Computing (Prodi Sistem Informasi - Universitas Trunojoyo Madura).

Aplikasi web pelaporan barang hilang dan ditemukan (**Lost & Found**) berbasis **Single Page Application (SPA)** yang didesain untuk arsitektur multi-VM terdistribusi menggunakan **Oracle VM VirtualBox (Type-2 Hypervisor)**, Docker Containerization, dan Nginx Load Balancing.

---

## 🏗️ Topologi Arsitektur VirtualBox Multi-VM

* **Physical Host:** Laptop MSI (Intel Core i7-13620H, 16 GB RAM, Windows 11)
* **Hypervisor:** Oracle VM VirtualBox 7.x
* **Jaringan:** Host-Only Adapter (`Subnet 192.168.56.0/24`)

| Node / Virtual Machine | IP Address | Peran & Layanan Utama |
| :--- | :--- | :--- |
| **VM 1: Frontend Server** | `192.168.56.101` | Nginx Web Server menyajikan React SPA (`dist/`) |
| **VM 2: Backend Cluster** | `192.168.56.102` | Nginx Load Balancer (Port 80) + 2x Container Docker Backend |
| **VM 3: Database Server** | `192.168.56.103` | Container Docker MySQL 8 dengan Persistent Storage Volume |

---

## 📁 Struktur Direktori Proyek

```
CC PAK FIRMAN/
├── lost-and-found-docs/    # Dokumentasi lengkap proyek
│   ├── design.md           # Topologi VirtualBox, ERD, dan spesifikasi API
│   ├── tech-stack.md       # Rationale teknologi, spek hardware & efisiensi RAM
│   ├── features.md         # Fitur aplikasi & skenario uji live demo dosen
│   └── plan.md             # Rencana kerja 5 fase & matriks RACI tim
├── database/               # Skema basis data
│   └── init.sql            # Script inisialisasi tabel items & seed data
├── backend/                # REST API (Node.js + Express)
│   ├── server.js           # Server utama + endpoint /api/health
│   ├── db.js               # Database abstraction & fallback
│   ├── package.json        # Dependensi Express, mysql2, cors
│   └── .env                # Variabel lingkungan
└── frontend/               # Single Page Application (React + Vite + Tailwind)
    ├── src/                # Komponen UI responsif & Cloud Inspector footer
    └── package.json        # Dependensi React, Lucide, Tailwind
```

---

## 🚀 Panduan Menjalankan di Komputer Lokal (Fase 1 Testing)

### 1. Menjalankan Backend API
Buka Terminal / PowerShell 1:
```powershell
cd backend
npm start
```
* Backend aktif di: `http://localhost:5000`
* Cek Health & Metadata Node: `http://localhost:5000/api/health`

### 2. Menjalankan Frontend SPA
Buka Terminal / PowerShell 2:
```powershell
cd frontend
npm run dev
```
* Buka browser dan akses: `http://localhost:3000`

---

## 👥 Tim Pengembang (5 Anggota)
* **Anggota 1 (Ketua / User):** Cloud Infrastructure & Network Lead (Setup VirtualBox & 3 VM)
* **Anggota 2:** Backend & Containerization Specialist (Dockerizing API & Multi-Instance)
* **Anggota 3:** Load Balancer & Reverse Proxy Engineer (Nginx Load Balancer di VM 2)
* **Anggota 4:** Database & Frontend Deployment Specialist (MySQL Container di VM 3 & Frontend Nginx di VM 1)
* **Anggota 5:** QA, Stress Testing & Documentation Lead (Pengujian Failover, Laporan & Live Demo)
