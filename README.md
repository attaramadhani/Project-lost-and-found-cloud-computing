# Campus Lost & Found: Cloud Computing Project

Proyek Final Mata Kuliah Cloud Computing  
Program Studi Sistem Informasi, Fakultas Teknik, Universitas Trunojoyo Madura  
Dosen Pengampu: **Firmansyah Adiputra, S.T., M.Sc.**

---

## Tim Pengembang & Pembagian Tugas

Sesuai ketentuan evaluasi tugas agar setiap anggota berkontribusi pada lapisan sistem yang jelas, tim membagi peran, tanggung jawab, dan berkas sebagai berikut:

| No | Nama Lengkap | NIM | Peran | Fokus Tugas Utama | Berkas yang Dikelola |
|:--:|:---|:---:|:---|:---|:---|
| 1 | Attala Alif Ramadhani Tri Hida | 230441100144 | Ketua Kelompok & Cloud Infrastructure Lead | Setup hypervisor VirtualBox di laptop host, konfigurasi Host-Only Network, pembuatan 3 VM Ubuntu Server, IP statis, dan pembukaan/penutupan presentasi | `lost-and-found-docs/design.md`, `lost-and-found-docs/tech-stack.md`, `PANDUAN_TEKNIS_TAHAP_1_DAN_6_*` |
| 2 | Tanji | 230441100045 | Database & Frontend Deployment Specialist | Setup container MySQL 8 dengan persistent volume di VM3, impor `init.sql`, build SPA React (`npm run build`), dan setup Nginx di VM1 | `database/init.sql`, `database/docker-compose.yml`, `frontend/nginx.conf`, `PANDUAN_TEKNIS_TAHAP_2_*` |
| 3 | Naufal Husain | 240441100038 | Backend & Containerization Specialist | REST API Express.js, Dockerfile backend, dan orkestrasi minimal 2 container backend (`backend-node-1` dan `backend-node-2`) via Docker Compose di VM2 | `backend/server.js`, `backend/Dockerfile`, `backend/docker-compose.yml`, `PANDUAN_TEKNIS_TAHAP_3_*` |
| 4 | Muhammad Naufal Widiatmoko | 230441100125 | Load Balancer & Reverse Proxy Engineer | Setup Nginx Load Balancer di VM2 (port 80), konfigurasi `upstream` Round-Robin, parameter failover, dan pencegahan header CORS ganda | `backend/nginx-lb.conf`, `PANDUAN_TEKNIS_TAHAP_4_*` |
| 5 | Moh. Yoga Dwi Prasetyo | 240441100133 | QA, Testing & Documentation Lead | Pengujian fungsional CRUD, uji load balancing, uji chaos failover, pengumpulan bukti tangkapan layar, laporan akhir Word, dan presentasi | `lost-and-found-docs/features.md`, `lost-and-found-docs/plan.md`, `LAPORAN_FINAL_PROJECT_CLOUD_COMPUTING.docx`, `PRESENTASI_FINAL_PROJECT_CLOUD_COMPUTING.pptx` |

---

## Topologi Arsitektur VirtualBox Multi-VM (Type-2 Hypervisor)

Tim menerapkan arsitektur terdistribusi 3-tier di atas subnet privat **`192.168.56.0/24`** menggunakan Oracle VM VirtualBox pada satu laptop host Windows 11 (16 GB RAM):

```text
+----------------------------------------------------------------------------------------+
| PHYSICAL HOST: Laptop Windows 11 (16 GB RAM)                                           |
|                                                                                        |
|  +----------------------------------------------------------------------------------+  |
|  | HYPERVISOR (Type-2): Oracle VM VirtualBox (Host-Only Gateway: 192.168.56.1)      |  |
|  +-------------------+--------------------------+--------------------------+--------+  |
|                      |                          |                          |           |
|                      v                          v                          v           |
|  +------------------------+ +----------------------------------+ +-------------------+ |
|  | VM 1: FRONTEND         | | VM 2: BACKEND CLUSTER            | | VM 3: DATABASE    | |
|  | IP: 192.168.56.101     | | IP: 192.168.56.102               | | IP: 192.168.56.103| |
|  | RAM: 1.5 GB (1 vCPU)   | | RAM: 2.0 GB (2 vCPU)             | | RAM: 1.5 GB       | |
|  |                        | |                                  | |                   | |
|  | Nginx Web Server (:80) | | Nginx Load Balancer (:80)        | | Docker MySQL 8    | |
|  | Serving React SPA      | | (Round-Robin + Failover)         | | (Port 3306)       | |
|  | (/var/www/html)        | |           |            |         | |                   | |
|  |                        | |   +-------+--------+   |         | | Named Volume:     | |
|  |                        | |   v                v   v         | | /var/lib/mysql    | |
|  |                        | | node-1 (:5001)  node-2 (:5002)   | | (Data Persisten)  | |
|  +------------------------+ +-----------+----------------------+ +---------+---------+ |
|                      ^                  |                                  |           |
|                      |                  +----------- Query SQL ------------+           |
|                      | Request REST API (/api/*)                                       |
|                      +-----------------------------------------------------------------+
+----------------------------------------^-----------------------------------------------+
                                         | Buka Browser Host: http://192.168.56.101
                           [ Pengguna / Dosen Penguji ]
```

---

## Ringkasan Antarmuka Aplikasi (Frontend SPA)

Antarmuka web di `frontend/` dibangun dengan **React 18, Vite 5, dan Tailwind CSS 3** menggunakan desain **Swiss Campus Ledger**:

- **Masthead & Ringkasan Real-Time:** Menampilkan judul portal dan ringkasan langsung jumlah laporan `Hilang`, `Ditemukan`, dan `Selesai` dari hasil API.
- **Pencarian & Filter Instan:** Filter tab status (`Semua Laporan`, `Barang Hilang`, `Barang Ditemukan`, `Selesai`), dropdown kategori, serta pencarian teks tanpa reload halaman.
- **Kartu Laporan & Konfirmasi Inline:** Kartu aktif terbaru tampil lebih lebar pada desktop, dilengkapi tombol `Hubungi via WhatsApp`, tombol `Tandai Selesai`, serta konfirmasi hapus inline (`Hapus laporan ini?`).
- **Modal Pelaporan Aksesibel:** Dialog `Buat Laporan Barang` mendukung penutupan dengan tombol `Escape`, label terikat pada setiap input, serta pesan error di dalam form.
- **Mode Terang & Mode Gelap:** Tombol pengalih tema di header mengubah tampilan secara langsung dan menyimpan pilihan di browser.
- **Monitor Node & Load Balancer:** Panel footer menampilkan container backend yang melayani (`served_by`), hostname, status koneksi MySQL VM3, tombol `Tes Ping Load Balancer`, dan riwayat ping pada sesi berjalan.

---

## Panduan Teknis Per Lapisan

### 1. Attala Alif Ramadhani Tri Hida (Cloud Infrastructure Lead)
* Memasang Oracle VM VirtualBox di host Windows 11.
* Mengaktifkan **Host-Only Network Adapter** dengan IP gateway `192.168.56.1` dan netmask `255.255.255.0`.
* Menyiapkan 3 VM **Ubuntu Server 22.04 LTS** (`VM1-Frontend`, `VM2-Backend`, `VM3-Database`) dengan dua NIC per VM: Adapter 1 NAT (akses internet saat instalasi) dan Adapter 2 Host-Only (IP statis `.101`, `.102`, `.103` via Netplan).

### 2. Tanji (Database & Frontend Deployment Specialist)
* **Di VM3 (Database Server: `192.168.56.103`):**
  Menjalankan container MySQL 8.0 menggunakan Docker Compose dengan named volume `lost_found_mysql_data` yang di-mount ke `/var/lib/mysql` agar data tabel `items` tidak hilang saat container dihapus atau dibuat ulang.
  ```bash
  cd database
  docker compose up -d
  docker ps
  docker volume ls
  ```
* **Di VM1 (Frontend Server: `192.168.56.101`):**
  Memastikan `frontend/.env` mengarah ke `VITE_API_URL=http://192.168.56.102/api`, menjalankan `npm run build` untuk menghasilkan `frontend/dist/`, menyalin isinya ke `/var/www/html/`, dan memasang `frontend/nginx.conf`.
  ```bash
  sudo apt install nginx -y
  sudo cp -r frontend/dist/* /var/www/html/
  sudo cp frontend/nginx.conf /etc/nginx/sites-available/default
  sudo systemctl restart nginx
  ```

### 3. Naufal Husain (Backend & Containerization Specialist)
* Mengemas API Express.js (`backend/server.js`) dengan `backend/Dockerfile` berbasis `node:20-alpine`, lalu menjalankan dua instance container (`backend-node-1` di port `5001:5000` dan `backend-node-2` di port `5002:5000`) melalui `backend/docker-compose.yml` di VM2 agar tidak ada *Single Point of Failure*.
  ```bash
  cd backend
  docker compose up -d --build
  docker ps
  ```

### 4. Muhammad Naufal Widiatmoko (Load Balancer & Reverse Proxy Engineer)
* Memasang `backend/nginx-lb.conf` pada port `80` VM2 untuk membagi beban ke `127.0.0.1:5001` dan `127.0.0.1:5002` secara Round-Robin, dengan parameter failover `max_fails=2 fail_timeout=5s`, `proxy_connect_timeout 2s`, dan `proxy_next_upstream`. Header CORS ditangani langsung oleh middleware `cors()` di Express agar tidak muncul header duplikat.
  ```bash
  sudo apt install nginx -y
  sudo cp backend/nginx-lb.conf /etc/nginx/sites-available/default
  sudo nginx -t
  sudo systemctl restart nginx
  sudo systemctl status nginx
  ```

### 5. Moh. Yoga Dwi Prasetyo (QA, Testing & Documentation Lead)
1. **Uji CRUD & UI:** Membuka `http://192.168.56.101`, menambah laporan baru lewat modal `Buat Laporan Barang`, menyegarkan halaman untuk memastikan data persisten di MySQL VM3, serta menguji filter, `Tandai Selesai`, hapus inline, dan mode terang/gelap.
2. **Uji Load Balancing Round-Robin:** Menjalankan loop request dari PowerShell host:
   ```powershell
   1..6 | ForEach-Object { (Invoke-RestMethod -Uri "http://192.168.56.102/api/health").served_by }
   ```
3. **Uji Chaos Failover:** Menghentikan `backend-node-1` (`docker stop backend-node-1`) di VM2, memverifikasi aplikasi web dan `/api/health` tetap merespons HTTP 200 melalui `backend-node-2`, lalu menyalakan kembali (`docker start backend-node-1`).
4. **Dokumentasi:** Menyusun bukti tangkapan layar dan laporan akhir resmi ([LAPORAN_FINAL_PROJECT_CLOUD_COMPUTING.docx](LAPORAN_FINAL_PROJECT_CLOUD_COMPUTING.docx), Bab I sampai Bab VII) serta dek presentasi ([PRESENTASI_FINAL_PROJECT_CLOUD_COMPUTING.pptx](PRESENTASI_FINAL_PROJECT_CLOUD_COMPUTING.pptx)).

---

## Panduan Menjalankan di Komputer Lokal (Tanpa VM)

Untuk mencoba aplikasi secara lokal di laptop Windows (backend berjalan otomatis pada mode *in-memory fallback* jika MySQL tidak aktif):

### 1. Jalankan Backend API
Buka PowerShell 1:
```powershell
cd backend
npm install
npm start
```
* Health check: `http://localhost:5000/api/health`
* Daftar items: `http://localhost:5000/api/items`

### 2. Jalankan Frontend SPA
Buka PowerShell 2, lalu timpa sementara `VITE_API_URL` agar mengarah ke backend lokal (karena `frontend/.env` bawaan mengarah ke IP VM2 `192.168.56.102`):
```powershell
cd frontend
npm install
$env:VITE_API_URL="http://localhost:5000/api"
npm run dev
```
* Buka browser ke `http://localhost:3000` (sesuai konfigurasi `frontend/vite.config.js`).

---

## Struktur Direktori Repositori

```text
CC PAK FIRMAN/
├── LAPORAN_FINAL_PROJECT_CLOUD_COMPUTING.docx                # Laporan resmi akademik (Bab I - VII)
├── PRESENTASI_FINAL_PROJECT_CLOUD_COMPUTING.pptx             # Slide presentasi final project (18 slide)
├── LAPORAN_PANDUAN_LIVE_DEMO_CLOUD_COMPUTING.docx            # Panduan skenario live demo
├── PANDUAN_TEKNIS_TAHAP_1_DAN_6_CLOUD_INFRASTRUCTURE_ATTALA.docx
├── PANDUAN_TEKNIS_TAHAP_2_DATABASE_PERSISTENT_STORAGE_TANJI.docx
├── PANDUAN_TEKNIS_TAHAP_3_BACKEND_CLUSTER_DOCKER.docx
├── PANDUAN_TEKNIS_TAHAP_4_LOAD_BALANCER_ROUND_ROBIN_WIDIATMOKO.docx
├── PANDUAN_TEKNIS_TAHAP_5_WEB_SPA_CRUD_DAN_CHAOS_FAILOVER_YOGA.docx
├── lost-and-found-docs/       # Dokumentasi desain sistem
│   ├── design.md              # Topologi VirtualBox, skema DB, dan kontrak REST API
│   ├── tech-stack.md          # Pilihan teknologi dan alokasi resource VM
│   ├── features.md            # Spesifikasi fitur aplikasi & skenario uji
│   └── plan.md                # Rencana kerja dan pembagian tugas
├── database/                  # Komponen basis data (VM3)
│   ├── init.sql               # Skema tabel items dan data awal
│   └── docker-compose.yml     # Container MySQL 8.0 + named volume
├── backend/                   # Komponen REST API & Load Balancer (VM2)
│   ├── server.js              # REST API Express + header X-Served-By
│   ├── db.js                  # Koneksi MySQL + mode fallback lokal
│   ├── Dockerfile             # Image Node.js 20 Alpine
│   ├── docker-compose.yml     # Orkestrasi 2 container backend
│   └── nginx-lb.conf          # Konfigurasi Nginx Round-Robin & failover
├── frontend/                  # Komponen Frontend SPA (VM1)
│   ├── src/                   # Kode sumber React + Tailwind CSS
│   ├── dist/                  # Hasil build produksi siap deploy ke /var/www/html
│   ├── nginx.conf             # Konfigurasi Nginx static SPA
│   ├── vite.config.js         # Konfigurasi dev server (port 3000)
│   └── package.json           # Dependensi frontend
└── screenshots/               # Arsip bukti tangkapan layar per kategori
    ├── 01_Arsitektur_dan_Ketentuan/
    ├── 02_VM1_Frontend_SPA/
    ├── 03_VM2_Backend_Cluster_LoadBalancer/
    ├── 04_VM3_Database_Persistent_Storage/
    ├── 05_Pengujian_LoadBalancing_dan_Failover/
    └── 06_Arsip_Instalasi_VirtualBox/
```

---

## Panduan Bukti Dokumentasi

Folder `screenshots/` menyimpan bukti tangkapan layar yang dikelompokkan per lapisan sistem:
* **01_Arsitektur_dan_Ketentuan:** Slide ketentuan tugas, diagram arsitektur 3-tier, dan topologi VirtualBox.
* **02_VM1_Frontend_SPA:** IP statis VM1 (`192.168.56.101`), status Nginx port 80, berkas build SPA, dan tangkapan layar aplikasi.
* **03_VM2_Backend_Cluster_LoadBalancer:** IP statis VM2 (`192.168.56.102`), konfigurasi `docker-compose.yml`, status `docker ps`, dan konfigurasi Nginx Load Balancer.
* **04_VM3_Database_Persistent_Storage:** IP statis VM3 (`192.168.56.103`), container MySQL 8.0 port 3306, named volume `lost_found_mysql_data`, dan hasil query tabel `items`.
* **05_Pengujian_LoadBalancing_dan_Failover:** Hasil `Test-Connection` ke 3 VM, uji Round-Robin 50:50, uji failover saat `backend-node-1` mati, dan uji pemulihan layanan.
* **06_Arsip_Instalasi_VirtualBox:** Arsip instalasi Ubuntu Server di VirtualBox.

Pemetaan detail bukti tangkapan layar tersedia di [`screenshots/README.md`](screenshots/README.md).
