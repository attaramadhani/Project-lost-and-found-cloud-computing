# 🌐 Campus Lost & Found — Cloud Computing Project

> **Proyek Final Mata Kuliah Cloud Computing**  
> Program Studi Sistem Informasi — Fakultas Teknik — Universitas Trunojoyo Madura  
> Dosen Pengampu: **Firmansyah Adiputra**

---

## 👥 Tim Pengembang & Pembagian Tugas Resmi

Sesuai ketentuan evaluasi tugas (*"setiap anggota harus memiliki kontribusi yang jelas"*), berikut adalah pembagian peran, tanggung jawab, dan berkas yang dikelola oleh masing-masing anggota:

| No | Nama Lengkap | NIM | Peran (Role) | Fokus Tugas Utama | Berkas yang Dikelola |
|:--:|:---|:---:|:---|:---|:---|
| **1** | **Attala Alif Ramadhani Tri Hida** | **230441100144** | **Ketua Kelompok & Cloud Infrastructure Lead** | Setup Hypervisor VirtualBox di host laptop, konfigurasi Host-Only Network, provisioning 3 VM Ubuntu Server, IP statis & firewall. | `lost-and-found-docs/design.md`, `lost-and-found-docs/tech-stack.md` |
| **2** | **Naufal Husain** | **240441100038** | **Backend & Containerization Specialist** | REST API Express.js, Dockerfile backend, setup **minimal 2 instance container backend** (`backend-1` & `backend-2`) via Docker Compose di VM 2. | `backend/server.js`, `backend/Dockerfile`, `backend/docker-compose.yml` |
| **3** | **Muhammad Naufal Widiatmoko** | **230441100125** | **Load Balancer & Reverse Proxy Engineer** | Setup Nginx Load Balancer di VM 2 (Port 80), konfigurasi `upstream` Round-Robin, failover timeout, dan header CORS. | `backend/nginx-lb.conf` |
| **4** | **Tanji** | **230441100045** | **Database & Frontend Deployment Specialist** | Setup container MySQL 8 dengan Persistent Volume di VM 3, import `init.sql`, build SPA React (`npm run build`), & setup Nginx di VM 1. | `database/init.sql`, `database/docker-compose.yml`, `frontend/nginx.conf` |
| **5** | **Moh. Yoga Dwi Prasetyo** | **240441100133** | **QA, Stress Testing & Documentation Lead** | Pengujian fungsional CRUD, uji load balancing cURL loop, uji failover (mematikan kontainer), dokumentasi screenshot, & laporan akhir. | `lost-and-found-docs/features.md`, `lost-and-found-docs/plan.md`, Laporan Word |

---

## 🏗️ Topologi Arsitektur VirtualBox Multi-VM (Type-2 Hypervisor)

Sistem dirancang mengimplementasikan konsep arsitektur cloud terdistribusi (*decoupling*) pada subnet lokal **`192.168.56.0/24`** yang berjalan 100% mandiri di atas laptop fisik (Host):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PHYSICAL HOST: Laptop MSI (Intel Core i7-13620H, 16 GB RAM, Windows 11)                │
│                                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ HYPERVISOR: Oracle VM VirtualBox (Host-Only Adapter: 192.168.56.1)               │  │
│  └───────────────────┬──────────────────────────┬──────────────────────────┬────────┘  │
│                      │                          │                          │           │
│                      ▼                          ▼                          ▼           │
│  ┌────────────────────────┐ ┌──────────────────────────────────┐ ┌───────────────────┐ │
│  │ VM 1: FRONT-END        │ │ VM 2: BACK-END CLUSTER           │ │ VM 3: DATABASE    │ │
│  │ IP: 192.168.56.101     │ │ IP: 192.168.56.102               │ │ IP: 192.168.56.103│ │
│  │ RAM: 1.0 GB            │ │ RAM: 1.5 GB                      │ │ RAM: 1.0 GB       │ │
│  │                        │ │                                  │ │                   │ │
│  │ Web Server (Nginx)     │ │ Nginx Load Balancer (Port 80)    │ │ Docker MySQL 8    │ │
│  │ Serving React SPA      │ │ (Algoritma Round-Robin + Failover│ │ (Port 3306)       │ │
│  │ (Folder /var/www/html) │ │            │            │        │ │                   │ │
│  │                        │ │   ┌────────┴────────┐   │        │ │ Persistent Volume:│ │
│  │                        │ │   ▼                 ▼   │        │ │ /var/lib/mysql    │ │
│  │                        │ │ Container 1   Container 2        │ │ (Data Anti Hilang)│ │
│  │                        │ │ (Port 5001)   (Port 5002)        │ │                   │ │
│  └────────────────────────┘ └───────────┬──────────────────────┘ └─────────▲─────────┘ │
│                      ▲                  │                                  │           │
│                      │                  └────────── Query SQL ─────────────┘           │
│                      │ Request API (/api/*)                                            │
│                      └─────────────────────────────────────────────────────────────────┘
└────────────────────────────────────────▲───────────────────────────────────────────────┘
                                         │ Buka Browser Host: http://192.168.56.101
                           [ Pengguna / Dosen Penguji ]
```

---

## 📖 Panduan Detail Pelaksanaan Tugas Per Anggota

Agar masing-masing anggota paham apa yang harus dipelajari dan dikerjakan, berikut panduan operasional langkah demi langkah:

---

### 👤 1. Attala Alif Ramadhani Tri Hida (Ketua & Infra Lead)
* **Konsep Dasar:** Virtualisasi server menggunakan Hypervisor Type-2 (VirtualBox) untuk membagi resource fisik CPU dan RAM laptop menjadi beberapa mesin virtual (VM) terisolasi.
* **Tanggung Jawab:**
  1. Menginstal Oracle VM VirtualBox di laptop Windows.
  2. Mengaktifkan **Host-Only Network Adapter** dengan IP Gateway `192.168.56.1` netmask `255.255.255.0`.
  3. Menginstal sistem operasi **Ubuntu Server 22.04 LTS** pada `VM1-Frontend`.
  4. Memanfaatkan fitur **Clone VirtualBox** untuk menduplikasi VM1 menjadi `VM2-Backend` dan `VM3-Database` dalam hitungan menit.
  5. Mengatur IP Statis di ketiga VM (`.101`, `.102`, `.103`) dan menguji `ping` antar-VM.
* **Bukti Screenshot untuk Laporan:**
  * Dashboard VirtualBox yang memperlihatkan ketiga VM berstatus *Running*.
  * Konfigurasi VirtualBox Network Tools (Host-Only Ethernet Adapter).
  * Output perintah `ip a` di masing-masing VM dan hasil `ping` antar-VM.

---

### 👤 2. Naufal Husain (Backend & Containerization Specialist)
* **Konsep Dasar: Apa itu "Minimal 2 Instance Application Server"?**
  * Dosen **melarang** backend hanya dijalankan 1 proses saja. Jika hanya 1 proses dan server tersebut *crash*, seluruh website akan mati (*Single Point of Failure*).
  * Maka, aplikasi backend Express.js dijalankan **sebanyak 2 kontainer kembar** (`backend-node-1` dan `backend-node-2`) yang aktif bersamaan di dalam **VM 2**.
* **Berkas yang Dipelajari:**
  * `backend/server.js`: Mengetahui endpoint `/api/health` yang mengembalikan nama kontainer (`served_by`) dan `/api/items` (CRUD).
  * `backend/Dockerfile`: Perintah pengemasan aplikasi Node.js ke Docker image berbasis `node:20-alpine`.
  * `backend/docker-compose.yml`: Skrip orkestrasi untuk menjalankan 2 instance backend:
    ```yaml
    services:
      backend-1:
        container_name: backend-node-1
        ports: ["5001:5000"]
        environment:
          - APP_INSTANCE=backend-node-1
          - DB_HOST=192.168.56.103
      backend-2:
        container_name: backend-node-2
        ports: ["5002:5000"]
        environment:
          - APP_INSTANCE=backend-node-2
          - DB_HOST=192.168.56.103
    ```
* **Perintah yang Dijalankan di VM 2:**
  ```bash
  cd backend
  docker compose up -d
  docker ps   # Memastikan kedua kontainer Up di port 5001 dan 5002
  ```
* **Bukti Screenshot untuk Laporan:**
  * Kode `backend/Dockerfile` dan `backend/docker-compose.yml`.
  * Output terminal `docker ps` di VM 2 yang menampilkan 2 kontainer backend aktif.

---

### 👤 3. Muhammad Naufal Widiatmoko (Load Balancer & Reverse Proxy Engineer)
* **Konsep Dasar: Bagaimana Load Balancer & Failover Bekerja?**
  * Karena ada 2 instance backend (port 5001 dan port 5002), Nginx dipasang di port 80 VM 2 sebagai gerbang utama.
  * **Bagi Beban (Round-Robin):** Request ganjil dikirim ke kontainer 1, request genap dikirim ke kontainer 2.
  * **Pengalihan Otomatis (Failover / High Availability):** Jika kontainer 1 mati, Nginx dalam hitungan milidetik langsung mengalihkan seluruh traffic ke kontainer 2 tanpa membuat website error.
* **Berkas yang Dipelajari:**
  * `backend/nginx-lb.conf`:
    ```nginx
    upstream backend_cluster {
        server 127.0.0.1:5001 max_fails=2 fail_timeout=10s;
        server 127.0.0.1:5002 max_fails=2 fail_timeout=10s;
    }
    server {
        listen 80;
        location /api/ {
            proxy_pass http://backend_cluster;
            proxy_next_upstream error timeout http_500 http_502 http_503;
        }
    }
    ```
* **Perintah yang Dijalankan di VM 2:**
  ```bash
  sudo apt install nginx -y
  sudo cp backend/nginx-lb.conf /etc/nginx/sites-available/default
  sudo nginx -t                # Uji validitas konfigurasi
  sudo systemctl restart nginx
  sudo systemctl status nginx
  ```
* **Bukti Screenshot untuk Laporan:**
  * File konfigurasi `nginx-lb.conf` bagian `upstream` dan `proxy_pass`.
  * Output status `systemctl status nginx` berwarna hijau (*active/running*).

---

### 👤 4. Tanji (Database & Frontend Deployment Specialist)
* **Konsep Dasar: Mengapa Database Harus di VM Terpisah & Butuh Persistent Volume?**
  * Sesuai ketentuan dosen: *"Deploy database pada VM yang berbeda sebagai container"*.
  * Jika kontainer MySQL dimatikan atau di-restart, secara default data di dalamnya akan terhapus. Oleh karena itu, kita wajib menggunakan **Docker Persistent Volume** (`-v mysql_storage:/var/lib/mysql`) agar data laporan barang hilang tetap tersimpan aman di disk VM 3.
* **Berkas yang Dipelajari:**
  * `database/init.sql`: Berisi perintah pembuatan database `lost_found_db`, tabel `items`, dan 4 data contoh awal.
  * `database/docker-compose.yml`: Konfigurasi kontainer MySQL 8 dengan volume storage persisten.
  * `frontend/nginx.conf`: Konfigurasi web server Nginx di VM 1 untuk melayani file SPA React (`dist/`).
* **Perintah yang Dijalankan:**
  * **Di VM 3 (Database Server: `192.168.56.103`):**
    ```bash
    cd database
    docker compose up -d
    docker ps                      # Pastikan MySQL aktif di port 3306
    docker volume ls               # Membuktikan volume lost_found_mysql_data ada
    ```
  * **Di VM 1 (Frontend Server: `192.168.56.101`):**
    ```bash
    sudo apt install nginx -y
    # Copy folder frontend/dist hasil build ke /var/www/html
    sudo cp -r frontend/dist/* /var/www/html/
    sudo cp frontend/nginx.conf /etc/nginx/sites-available/default
    sudo systemctl restart nginx
    ```
* **Bukti Screenshot untuk Laporan:**
  * Output `docker ps` dan `docker volume ls` di VM 3.
  * Hasil query SQL di terminal VM 3: `SELECT * FROM items;`.
  * File konfigurasi `frontend/nginx.conf` di VM 1.

---

### 👤 5. Moh. Yoga Dwi Prasetyo (QA, Testing & Documentation Lead)
* **Konsep Dasar: Pembuktian Ilmiah & Evaluasi Kriteria Dosen**
  * Dosen membutuhkan bukti otentik bahwa sistem benar-benar bekerja, memiliki load balancing, dan tahan terhadap kegagalan (*fault tolerant*).
* **Tanggung Jawab Pengujian & Dokumentasi:**
  1. **Uji 1 (CRUD Fungsional):** Buka browser laptop host ke `http://192.168.56.101`, isi formulir laporan barang baru $\rightarrow$ pastikan muncul di layar dan masuk ke database di VM 3. Ambil screenshot.
  2. **Uji 2 (Load Balancing Round-Robin):** Di terminal laptop host, jalankan perintah loop HTTP:
     ```powershell
     for ($i=1; $i -le 6; $i++) {
         (Invoke-RestMethod -Uri "http://192.168.56.102/api/health").served_by
     }
     ```
     Ambil screenshot output yang menunjukkan respons bergantian antara `backend-node-1` dan `backend-node-2`.
  3. **Uji 3 (Failover / Chaos Test — Poin Nilai A ⭐):**
     * Di terminal VM 2, matikan kontainer 1: `docker stop backend-node-1`.
     * Refresh website di browser host $\rightarrow$ buktikan website **TIDAK ERROR** dan tetap berjalan normal karena otomatis ditangani oleh `backend-node-2`. Ambil screenshot.
     * Nyalakan kembali: `docker start backend-node-1`.
  4. Mengumpulkan seluruh screenshot ke dalam draf **Laporan Akhir Word/PDF** (Bab 1 Pendahuluan, Bab 2 Arsitektur, Bab 3 Konfigurasi, Bab 4 Pengujian, Bab 5 Kesimpulan) dan menyusun slide PowerPoint presentasi.

---

## 💻 Panduan Menjalankan di Komputer Lokal (Uji Coba Cepat di Host)

Sebelum dideploy ke VirtualBox, seluruh kodingan aplikasi ini sudah bisa dicoba langsung di laptop host:

### 1. Menjalankan Backend API
Buka Terminal / PowerShell 1:
```powershell
cd backend
npm install
npm start
```
* API Health Check: `http://localhost:5000/api/health`
* Data Barang: `http://localhost:5000/api/items`

### 2. Menjalankan Frontend SPA
Buka Terminal / PowerShell 2:
```powershell
cd frontend
npm install
npm run dev
```
* Buka browser di: **`http://localhost:3000`**

---

## 📁 Struktur Direktori Repositori

```
CC PAK FIRMAN/
├── lost-and-found-docs/    # Dokumentasi lengkap proyek
│   ├── design.md           # Topologi VirtualBox, ERD, dan spesifikasi API
│   ├── tech-stack.md       # Rationale teknologi, spek hardware & alokasi RAM
│   ├── features.md         # Fitur aplikasi & skenario uji live demo dosen
│   └── plan.md             # Rencana kerja 5 fase & matriks RACI tim
├── database/               # Komponen basis data (VM 3)
│   ├── init.sql            # Script inisialisasi tabel items & seed data
│   └── docker-compose.yml  # Docker compose MySQL + persistent volume
├── backend/                # Komponen backend API & Load Balancer (VM 2)
│   ├── server.js           # REST API Express + penanda node served_by
│   ├── db.js               # Database abstraction & fallback
│   ├── Dockerfile          # Image builder Node.js 20 Alpine
│   ├── docker-compose.yml  # Multi-instance 2 container backend
│   └── nginx-lb.conf       # Konfigurasi Nginx Load Balancer Round-Robin
└── frontend/               # Komponen frontend SPA (VM 1)
    ├── src/                # Komponen antarmuka React + Tailwind
    ├── nginx.conf          # Konfigurasi Nginx untuk static SPA hosting
    └── package.json        # Dependensi React, Vite, Lucide
```
