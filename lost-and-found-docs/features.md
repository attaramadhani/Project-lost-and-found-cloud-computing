# Fitur Aplikasi & Skenario Pengujian: Campus Lost & Found (VirtualBox Setup)

Dokumen ini merinci daftar fitur fungsional aplikasi untuk pengguna, fitur arsitektur virtualisasi untuk penilaian dosen, serta panduan pengujian langsung (*live testing demo*) menggunakan topologi VirtualBox.

---

## 1. Fitur Fungsional Pengguna (User Features)

### A. Katalog & Feed Laporan (Single Page Application)
* **Kategori Tab Cepat:** Filter instan tanpa refresh halaman antara:
  * Semua Laporan
  * Barang Hilang (*Lost*) — aksen badge merah
  * Barang Ditemukan (*Found*) — aksen badge hijau
  * Kasus Selesai (*Resolved*) — aksen abu-abu
* **Pencarian Real-Time:** Filter dinamis berdasarkan nama barang, deskripsi, atau lokasi kejadian.
* **Filter Kategori Barang:** Dropdown pemilah: Dokumen/KTM, Kendaraan/Kunci, Elektronik, Pakaian/Aksesoris, dan Lain-lain.

### B. Formulir Pelaporan Cepat (Lapor Hilang / Temuan)
* Modal formulir SPA interaktif tanpa pergantian halaman.
* Form validasi: Nama barang, kategori, tanggal perkiraan, lokasi, deskripsi rinci, nama pelapor, dan nomor WhatsApp.

### C. Direct WhatsApp Action (One-Click Contact)
* Tombol "Hubungi via WA" pada setiap kartu barang yang langsung membuka tautan `https://wa.me/628xxx` dengan template teks otomatis terkait barang yang dimaksud.

### D. Penutupan Kasus (Mark as Resolved)
* Tombol untuk menandai barang yang sudah dikembalikan ke pemiliknya (`status: resolved`).

---

## 2. Fitur Arsitektur Virtualisasi (Kriteria Penilaian Dosen)

### A. Live Node Inspector (Bukti Nyata Load Balancing)
* Footer antarmuka menampilkan metadata backend:
  ```
  Handled by: backend-node-1 [Host: 4b291c90] | Round-Robin Active
  ```
* Saat tombol *"Tes Ping Load Balancer"* diklik atau halaman di-refresh, node akan bergantian secara nyata antara `backend-node-1` dan `backend-node-2`.

### B. Multi-Instance High Availability
* Dua kontainer Docker backend berjalan secara independen di dalam **VM 2 (192.168.56.102)** pada port `5001` dan `5002`.
* Nginx bertindak sebagai Load Balancer di port `80` untuk membagi traffic.

### C. Zero-Downtime Failover (Simulasi Gangguan Server)
* Jika kontainer pertama dimatikan paksa (`docker stop backend-node-1`), Nginx secara otomatis mendeteksi dan mengalihkan 100% permintaan ke kontainer kedua tanpa kegagalan koneksi bagi pengguna di browser.

### D. Persistent Database Storage
* Data tersimpan di dalam kontainer MySQL pada **VM 3 (192.168.56.103)** menggunakan Docker Volume (`-v mysql_data:/var/lib/mysql`).
* Data tetap aman dan utuh meskipun kontainer database dihentikan atau direstart.

### E. Isolasi Jaringan (Security Rule)
* Port `3306` MySQL di VM 3 hanya diizinkan untuk IP `192.168.56.102` (VM 2). Komputer Host Windows dan VM 1 tidak dapat mengakses langsung database ini demi kepatuhan prinsip keamanan jaringan.

---

## 3. Panduan Skenario Pengujian (Untuk Laporan & Live Demo)

Berikut adalah panduan langkah demi langkah saat melakukan live demo di depan dosen:

```
[ Browser Host Windows ] ──► Akses: http://192.168.56.101 (VM 1 Frontend)
                                             │
                                             ▼
[ Terminal SSH Host ]    ──► SSH ke: 192.168.56.102 (VM 2 Backend)
                         ──► SSH ke: 192.168.56.103 (VM 3 Database)
```

### Skenario 1: Uji Aliran Data End-to-End (CRUD)
1. Buka browser di laptop Host: akses `http://192.168.56.101`.
2. Klik tombol **"Lapor Barang"**, isi data barang baru (misal: "KTM An. Budi"), lalu klik kirim.
3. Buka terminal PowerShell di laptop Host, lakukan SSH ke VM 3:
   ```bash
   ssh user@192.168.56.103
   docker exec -it mysql-server mysql -u root -p lost_found_db -e "SELECT * FROM items;"
   ```
4. **Hasil yang dibuktikan:** Data baru yang diinput di VM 1 langsung tersimpan secara aman di database VM 3.

### Skenario 2: Uji Pembuktian Load Balancing (Round-Robin)
1. Di terminal laptop Host, jalankan loop permintaan HTTP ke IP VM 2:
   ```powershell
   for ($i=1; $i -le 6; $i++) {
       (Invoke-RestMethod -Uri "http://192.168.56.102/api/health").served_by
   }
   ```
2. **Hasil yang diharapkan:**
   ```
   backend-node-1
   backend-node-2
   backend-node-1
   backend-node-2
   backend-node-1
   backend-node-2
   ```
   *(Tunjukkan output ini di depan dosen untuk membuktikan Load Balancer Nginx membagi beban 50:50).*

### Skenario 3: Uji Ketahanan Sistem (Chaos / Failover Test)
1. Di terminal SSH ke VM 2, matikan salah satu kontainer backend:
   ```bash
   docker stop backend-node-1
   ```
2. Buka browser di laptop Host (`http://192.168.56.101`), lakukan refresh dan coba tambahkan data.
3. **Hasil yang dibuktikan:** Website tetap berjalan normal tanpa error karena Nginx otomatis mengalihkan beban ke `backend-node-2`.
4. Nyalakan kembali kontainer:
   ```bash
   docker start backend-node-1
   ```
   Beban kembali dibagi secara bergantian.
