# Rencana Eksekusi & Roadmap: Campus Lost & Found (VirtualBox Setup)

Dokumen ini memuat rencana kerja operasional 5 fase, pembagian tugas harian untuk 5 anggota kelompok, serta matriks tanggung jawab (RACI) dengan skenario implementasi **Oracle VM VirtualBox (On-Premise Private Cloud)**.

---

## 1. Roadmap & Timeline Pengerjaan (5 Fase)

```
[Fase 1: Koding Lokal] ──► [Fase 2: Dockerization] ──► [Fase 3: Setup VirtualBox & 3 VM]
      (SELESAI ✅)                (Hari 4-5)                        (Hari 6-8)
                                                                        │
[Fase 5: Laporan & Live Demo] ◄── [Fase 4: Deployment ke 3 VM] ◄────────┘
         (Hari 14-17)                       (Hari 9-13)
```

---

### FASE 1: Inisiasi & Pembuatan Kode Dasar Lokal (SELESAI ✅)
*Tujuan: Memiliki kode aplikasi SPA, REST API, dan Skema Database yang siap pakai.*
* [x] **Langkah 1.1:** Skema database MySQL & data awal di [`database/init.sql`](file:///C:/Users/Atta/OneDrive/Documents/CC%20PAK%20FIRMAN/database/init.sql).
* [x] **Langkah 1.2:** Backend Node.js Express REST API di [`backend/`](file:///C:/Users/Atta/OneDrive/Documents/CC%20PAK%20FIRMAN/backend/) dengan endpoint `/api/health` dan `/api/items`.
* [x] **Langkah 1.3:** Frontend React SPA + Tailwind di [`frontend/`](file:///C:/Users/Atta/OneDrive/Documents/CC%20PAK%20FIRMAN/frontend/) dengan filter, search, form modal, WhatsApp CTA, dan Cloud Inspector footer.
* [x] **Langkah 1.4:** Uji coba end-to-end lokal di Windows: Berhasil 100%.

---

### FASE 2: Dockerization & Konfigurasi Container (Hari 4 – 5)
*Tujuan: Mengemas aplikasi ke dalam image Docker standar industri.*
* [ ] **Langkah 2.1 (Anggota 2):** Buat `Dockerfile` untuk Backend API (image ringan berbasis `node:20-alpine`).
* [ ] **Langkah 2.2 (Anggota 4):** Buat `Dockerfile` untuk Frontend SPA (multi-stage build: build Vite lalu serve via Nginx alpine).
* [ ] **Langkah 2.3 (Anggota 2 & 3):** Buat `docker-compose.yml` backend cluster untuk menjalankan 2 container backend (`backend-1` port `5001`, `backend-2` port `5002`).
* [ ] **Langkah 2.4 (Anggota 3):** Siapkan file konfigurasi Nginx Load Balancer (`nginx.conf`) dengan directive upstream Round-Robin.

---

### FASE 3: Setup Hypervisor & Provisioning 3 VM di VirtualBox (Hari 6 – 8)
*Tujuan: Mempersiapkan lingkungan virtualisasi 3 VM di laptop host.*
* [ ] **Langkah 3.1 (Anggota 1):** Install **Oracle VM VirtualBox 7.x** di laptop host MSI Windows 11.
* [ ] **Langkah 3.2 (Anggota 1):** Konfigurasi **Host-Only Network** di VirtualBox Tools $\rightarrow$ Network:
  * Adapter: `192.168.56.1`
  * Netmask: `255.255.255.0`
  * DHCP Server: Diaktifkan atau dinonaktifkan (untuk IP statis).
* [ ] **Langkah 3.3 (Anggota 1):** Unduh ISO **Ubuntu Server 22.04 LTS Minimal** (tanpa GUI desktop).
* [ ] **Langkah 3.4 (Anggota 1):** Install **VM 1 Master** (1 vCPU, 1 GB RAM, Disk 10 GB). Install package dasar: `docker`, `docker-compose-plugin`, `nginx`, `net-tools`, `curl`.
* [ ] **Langkah 3.5 (Anggota 1):** Matikan VM 1, lalu gunakan fitur **Clone** VirtualBox untuk membuat:
  * **VM 2 (Backend Cluster):** Alokasi 2 vCPU, 1.5 GB RAM.
  * **VM 3 (Database Server):** Alokasi 1 vCPU, 1.0 GB RAM.
* [ ] **Langkah 3.6 (Anggota 1):** Konfigurasi static IP via Netplan di masing-masing VM:
  * `VM 1`: `192.168.56.101`
  * `VM 2`: `192.168.56.102`
  * `VM 3`: `192.168.56.103`
  * Tes saling ping antar-VM dan dari laptop Host Windows.

---

### FASE 4: Deployment Sistem ke 3 VM VirtualBox (Hari 9 – 13)
*Tujuan: Memindahkan kode dan menjalankan service di masing-masing VM.*

* [ ] **Langkah 4.1 (Anggota 4 - di VM 3: 192.168.56.103):**
  * Jalankan container MySQL dengan Persistent Volume:
    ```bash
    docker run -d --name mysql-server \
      -p 3306:3306 \
      -v mysql_data:/var/lib/mysql \
      -e MYSQL_ROOT_PASSWORD=rahasia123 \
      -e MYSQL_DATABASE=lost_found_db \
      --restart always mysql:8
    ```
  * Import file [`database/init.sql`](file:///C:/Users/Atta/OneDrive/Documents/CC%20PAK%20FIRMAN/database/init.sql) ke dalam container.
* [ ] **Langkah 4.2 (Anggota 2 - di VM 2: 192.168.56.102):**
  * Copy folder `backend/` ke VM 2. Atur file `.env`:
    ```env
    PORT=5000
    DB_HOST=192.168.56.103
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=rahasia123
    DB_NAME=lost_found_db
    ```
  * Jalankan 2 instance container backend via Docker Compose:
    * `backend-1` (port `5001`, `APP_INSTANCE=backend-node-1`)
    * `backend-2` (port `5002`, `APP_INSTANCE=backend-node-2`)
* [ ] **Langkah 4.3 (Anggota 3 - di VM 2: 192.168.56.102):**
  * Konfigurasi Nginx di VM 2 sebagai Load Balancer pada port `80`:
    ```nginx
    upstream backend_cluster {
        server 127.0.0.1:5001;
        server 127.0.0.1:5002;
    }
    server {
        listen 80;
        location /api/ {
            proxy_pass http://backend_cluster;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
  * Test dari host: `curl http://192.168.56.102/api/health`.
* [ ] **Langkah 4.4 (Anggota 4 - di VM 1: 192.168.56.101):**
  * Di `frontend/.env`, set `VITE_API_URL=http://192.168.56.102/api`.
  * Build project: `npm run build`.
  * Copy folder `dist/` ke VM 1 (`/var/www/html`).
  * Konfigurasi Nginx di VM 1 untuk serve file statis SPA di port `80`.

---

### FASE 5: Pengujian, Dokumentasi Laporan & Live Demo (Hari 14 – 17)
*Tujuan: Dokumentasi bukti pengujian dan gladi resik presentasi.*

* [ ] **Langkah 5.1 (Anggota 5):** Eksekusi pengujian sesuai skenario di [`features.md`](file:///C:/Users/Atta/OneDrive/Documents/CC%20PAK%20FIRMAN/lost-and-found-docs/features.md):
  * **Uji 1:** CRUD dari browser host `http://192.168.56.101` $\rightarrow$ data masuk ke DB di `192.168.56.103` (Screenshot).
  * **Uji 2:** Loop 10 request ke `192.168.56.102` $\rightarrow$ buktikan respon bergantian `backend-node-1` & `backend-node-2` (Screenshot).
  * **Uji 3 (Failover):** Matikan kontainer `backend-1` via terminal SSH $\rightarrow$ buktikan web tetap hidup via `backend-2` (Screenshot).
* [ ] **Langkah 5.2 (Anggota 5 & Anggota 1):** Susun Dokumen Laporan Akhir:
  * Bab 1: Pendahuluan & Pembagian Tugas Anggota.
  * Bab 2: Arsitektur Aplikasi & Arsitektur VirtualBox Multi-VM.
  * Bab 3: Konfigurasi Deployment (`Dockerfile`, `docker-compose`, `nginx.conf`, netplan IP).
  * Bab 4: Hasil Pengujian & Analisis Bukti Screenshot.
  * Bab 5: Kesimpulan.
* [ ] **Langkah 5.3 (Semua Anggota):** Latihan presentasi dan gladi resik demonstrasi langsung (*live testing*).

---

## 2. Matriks Tanggung Jawab Tim (RACI Matrix)

| Modul / Aktivitas | Anggota 1 (Infra Lead) | Anggota 2 (Backend Dev) | Anggota 3 (LB & Proxy) | Anggota 4 (FE & DB) | Anggota 5 (QA & Docs) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Setup VirtualBox & 3 VM Ubuntu Server | **R / A** | I | C | I | I |
| Konfigurasi Host-Only Network & Static IP | **R / A** | C | C | I | I |
| Dockerfile Backend & Docker-Compose (VM 2) | I | **R / A** | C | C | I |
| Konfigurasi Nginx Load Balancer (VM 2) | C | C | **R / A** | I | I |
| Setup DB Container & Persistent Volume (VM 3) | C | C | I | **R / A** | I |
| Build & Deploy Frontend Nginx SPA (VM 1) | I | I | C | **R / A** | I |
| Uji Load Balancing & Failover Chaos Test | I | C | C | I | **R / A** |
| Penyusunan Laporan Akhir & Slide Presentasi | C | C | C | C | **R / A** |

---

## 3. Checklist Kesiapan Sebelum Sidang Presentasi

1. [ ] VirtualBox aktif di laptop Host dengan ketiga VM running (**VM 1, VM 2, VM 3**).
2. [ ] Buka browser di laptop Host: `http://192.168.56.101` langsung menampilkan halaman web.
3. [ ] Footer Cloud Inspector menampilkan respon aktif dari Backend Node.
4. [ ] Jendela terminal SSH ke VM 2 (`192.168.56.102`) sudah standby untuk mendemokan perintah `docker ps` dan `docker stop` di depan Pak Firman.
5. [ ] Dokumen laporan tercetak/terkumpul rapi dengan seluruh screenshot pengujian.
