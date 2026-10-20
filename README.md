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

## 👥 Tim Pengembang & Pembagian Tugas (Kelompok CC)

| No | Nama Lengkap | NIM | Peran (Role) | Tanggung Jawab Utama |
|:--:|:---|:---:|:---|:---|
| **1** | **Attala Alif Ramadhani Tri Hida** | **230441100144** | **Ketua Kelompok & Cloud Infrastructure Lead** | • Setup Hypervisor VirtualBox di laptop host MSI.<br>• Konfigurasi Virtual Network (Host-Only `192.168.56.0/24`).<br>• Provisioning 3 VM Ubuntu Server (Master & Cloning).<br>• Konfigurasi static IP & firewall antar-VM. |
| **2** | **Naufal Husain** | **240441100038** | **Backend & Containerization Specialist** | • Mempersiapkan REST API Express.js & endpoint `/api/health`.<br>• Dockerizing API menggunakan `Dockerfile`.<br>• Menjalankan 2 instance Backend Container (`backend-1` & `backend-2`) via Docker Compose di VM 2.<br>• Integrasi penanda `served_by` untuk bukti load balancing. |
| **3** | **Muhammad Naufal Widiatmoko** | **230441100125** | **Load Balancer & Reverse Proxy Engineer** | • Instalasi & konfigurasi Nginx Load Balancer di VM 2 (Port 80).<br>• Implementasi algoritma Round-Robin ke port 5001 & 5002.<br>• Konfigurasi header CORS dan routing lalu lintas API. |
| **4** | **Tanji** | **230441100045** | **Database & Frontend Deployment Specialist** | • Deployment container Docker MySQL 8 di VM 3 dengan Persistent Volume.<br>• Import skema basis data & data awal (`init.sql`).<br>• Build Frontend React SPA (`npm run build`) & hosting via Nginx di VM 1. |
| **5** | **Moh. Yoga Dwi Prasetyo** | **240441100133** | **QA, Stress Testing & Documentation Lead** | • Pengujian fungsional end-to-end CRUD dari browser host.<br>• Pengujian Load Balancing (Round-Robin curl loop).<br>• Pengujian Failover Chaos Test (simulasi mematikan kontainer 1 di VM 2).<br>• Mengumpulkan bukti screenshot, menyusun Laporan Akhir & Slide Presentasi. |
