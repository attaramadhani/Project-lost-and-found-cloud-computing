# Teknologi & Rationale: Campus Lost & Found (VirtualBox Architecture)

Dokumen ini menguraikan daftar teknologi (*tech stack*) yang digunakan, spesifikasi perangkat keras laptop host, serta alasan pemilihannya pada lingkungan virtualisasi lokal (Hypervisor Type-2).

---

## 1. Spesifikasi Perangkat Keras Host (Physical Machine)

| Komponen | Spesifikasi Hardware Laptop | Keterangan untuk Tugas CC |
| :--- | :--- | :--- |
| **Brand & Model** | MSI Gaming / High Performance Laptop | Host fisik utama sistem |
| **Processor (CPU)**| **Intel Core i7-13620H (13th Gen)**<br>10 Cores, 16 Threads (up to 4.90 GHz) | Sangat bertenaga untuk menjalankan multi-core virtualization |
| **RAM Fisik** | **16.0 GB DDR5 / DDR4** | Kapasitas besar, mampu menampung 3 VM sekaligus tanpa penurunan performa OS Host |
| **Penyimpanan** | SSD NVMe (Tersisa **>480 GB Free**) | Waktu boot VM sangat cepat (<10 detik) |
| **Sistem Operasi** | Windows 11 Home 64-bit | Host OS yang menjalankan Hypervisor |

---

## 2. Ringkasan Tech Stack & Peran Komponen

| Lapisan (Layer) | Teknologi Terpilih | Versi | Peran Utama |
| :--- | :--- | :--- | :--- |
| **Physical Host** | Laptop MSI (i7 Gen 13, 16 GB RAM) | Hardware | Komputer fisik penyedia resource CPU, RAM, & Disk |
| **Hypervisor** | **Oracle VM VirtualBox** | 7.0+ | Type-2 Hypervisor untuk membagi dan mengisolasi 3 VM |
| **Virtual Network** | VirtualBox Host-Only Adapter | Subnet 192.168.56.x | Jaringan virtual privat terisolasi antar-VM dan host |
| **Guest OS** | Ubuntu Server (Headless/CLI) | 22.04 LTS | Sistem operasi ringan tanpa GUI untuk VM 1, 2, dan 3 |
| **Front-End** | React (Vite) + Tailwind CSS | React 18 | Single Page Application (SPA) responsif |
| **Web Server FE** | Nginx | 1.24+ | Web server statis untuk SPA di VM 1 |
| **Back-End API** | Node.js + Express.js | Node 20 LTS | RESTful API server pemroses logika bisnis CRUD |
| **Load Balancer** | Nginx | 1.24+ | Reverse proxy load balancing (algoritma Round-Robin) di VM 2 |
| **Database** | MySQL Server | 8.0 | Sistem basis data relasional di VM 3 |
| **Container Engine**| Docker Engine & Docker Compose | Docker 25+ | Menjalankan kontainer backend (VM 2) dan DB (VM 3) |

---

## 3. Alokasi Resource & Efisiensi RAM per VM

Karena kita menggunakan **Ubuntu Server 22.04 (versi teks tanpa desktop GUI)**, pemakaian sumber daya sangat efisien:

```
[ Total RAM Fisik Laptop: 16.0 GB ]
 ├── Windows 11 Host OS : ~4.5 GB
 ├── VM 1 (Frontend SPA):  1.0 GB  (IP: 192.168.56.101)
 ├── VM 2 (Backend + LB):  1.5 GB  (IP: 192.168.56.102)
 ├── VM 3 (Database DB) :  1.0 GB  (IP: 192.168.56.103)
 └── SISA FREE RAM      : ~8.0 GB  (Laptop tetap sangat dingin & lancar)
```

| Virtual Machine | Alokasi vCPU | Alokasi RAM | Pemakaian RAM Riil | Penyimpanan VDI |
| :--- | :---: | :---: | :---: | :---: |
| **VM 1: Frontend Server** | 1 Core | 1024 MB | ~150 MB (Nginx + OS) | ~6 GB |
| **VM 2: Backend Cluster** | 2 Core | 1536 MB | ~280 MB (2x Node.js + Nginx + OS) | ~8 GB |
| **VM 3: Database Server** | 1 Core | 1024 MB | ~450 MB (MySQL + OS) | ~8 GB |
| **TOTAL UNTUK 3 VM** | **4 Core** | **3.5 GB** | **~880 MB riil** | **~22 GB** |

---

## 4. Keuntungan Memilih VirtualBox Dibandingkan Public Cloud

1. **Bebas Masalah Verifikasi Pembayaran:** Menghindari sistem penolakan kartu otomatis seperti yang terjadi pada pendaftaran cloud publik (Oracle/AWS/GCP).
2. **Kemandirian Live Demo (Zero-Dependency):** Tidak bergantung pada koneksi internet kampus UTM yang sering membatasi port atau memiliki latensi tinggi.
3. **Penyelarasan Materi Kuliah:** Mengimplementasikan secara nyata teori Virtualisasi & Hypervisor dari Slide Pertemuan 02 (*Arsitektur Cloud: Physical Machine $\rightarrow$ Hypervisor $\rightarrow$ Multi-VM*).
4. **Kecepatan Replikasi (Cloning):** Cukup install 1 VM Master Ubuntu Server, lalu manfaatkan fitur **Linked / Full Clone** VirtualBox untuk membuat VM 2 dan VM 3 dalam hitungan menit.
