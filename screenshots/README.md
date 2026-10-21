# DOKUMENTASI LENGKAP FINAL PROJECT CLOUD COMPUTING
**Dosen Pengampu: Firmansyah Adiputra, S.T., M.Sc.**  
**Program Studi Sistem Informasi - Universitas Trunojoyo Madura**

---

## 📁 Struktur Folder Bukti Dokumentasi (Screenshots)

Folder ini telah distrukturisasi secara sistematis menjadi 6 folder utama yang 100% mematuhi ketentuan penugasan dan evaluasi pada slide materi kuliah:

```
screenshots/
├── 01_Arsitektur_dan_Ketentuan/
│   ├── 01_ketentuan_deployment_slide_kuliah.png
│   ├── 02_diagram_arsitektur_aplikasi_3tier.png
│   └── 03_diagram_topologi_deployment_multi_vm.png
├── 02_VM1_Frontend_SPA/
│   ├── 01_vm1_ip_statis_enp0s8.png
│   ├── 02_vm1_webserver_nginx_status.png
│   ├── 03_vm1_file_build_production_spa.png
│   ├── 04_browser_portal_lost_and_found_home.png
│   └── 05_browser_portal_lost_and_found_filter.png
├── 03_VM2_Backend_Cluster_LoadBalancer/
│   ├── 01_vm2_ip_statis_enp0s8.png
│   ├── 02_vm2_docker_compose_config.png
│   ├── 03_vm2_docker_ps_2_instances_running.png
│   ├── 04_vm2_nginx_loadbalancer_upstream_conf.png
│   └── 05_vm2_nginx_service_active.png
├── 04_VM3_Database_Persistent_Storage/
│   ├── 01_vm3_ip_statis_enp0s8.png
│   ├── 02_vm3_docker_compose_mysql.png
│   ├── 03_vm3_docker_ps_mysql_running.png
│   ├── 04_vm3_docker_volume_persistent.png
│   └── 05_vm3_mysql_query_select_items.png
├── 05_Pengujian_LoadBalancing_dan_Failover/
│   ├── 01_uji_konektivitas_ping_3_vm.png
│   ├── 02_uji_load_balancing_round_robin_curl.png
│   ├── 03_uji_failover_simulasi_node1_down.png
│   ├── 04_uji_failover_recovery_node1.png
│   └── 05_uji_rest_api_json_response.png
└── 06_Arsip_Instalasi_VirtualBox/
    ├── 01_persiapan_file_iso_ubuntu_dan_virtualbox.png
    └── ... (Foto wizard instalasi awal VM 01 s/d 12)
```

---

## 📌 Pemetaan Screenshot ke Bab Laporan Akhir

### BAB 1: Ketentuan & Arsitektur Sistem
* Gunakan folder `01_Arsitektur_dan_Ketentuan/`:
  - **Gambar 1.1:** `01_ketentuan_deployment_slide_kuliah.png` (Slide resmi tugas).
  - **Gambar 1.2:** `02_diagram_arsitektur_aplikasi_3tier.png` (Diagram 3-Tier: Presentation, Logic & LB, Data Storage).
  - **Gambar 1.3:** `03_diagram_topologi_deployment_multi_vm.png` (Diagram Jaringan 3 VM di Subnet 192.168.56.0/24).

### BAB 2: Konfigurasi VM 1 (Frontend SPA)
* Gunakan folder `02_VM1_Frontend_SPA/`:
  - **Gambar 2.1:** `01_vm1_ip_statis_enp0s8.png` (Alamat IP Statis 192.168.56.101).
  - **Gambar 2.2:** `02_vm1_webserver_nginx_status.png` (Nginx Web Server aktif melayani HTTP port 80).
  - **Gambar 2.3:** `03_vm1_file_build_production_spa.png` (File bundle SPA Vite di `/var/www/html`).
  - **Gambar 2.4:** `04_browser_portal_lost_and_found_home.png` (Tampilan antarmuka browser portal Lost & Found).
  - **Gambar 2.5:** `05_browser_portal_lost_and_found_filter.png` (Tampilan fitur filter kategori dan pencarian barang).

### BAB 3: Konfigurasi VM 2 (Backend Cluster & Load Balancer)
* Gunakan folder `03_VM2_Backend_Cluster_LoadBalancer/`:
  - **Gambar 3.1:** `01_vm2_ip_statis_enp0s8.png` (Alamat IP Statis 192.168.56.102).
  - **Gambar 3.2:** `02_vm2_docker_compose_config.png` (Konfigurasi minimal 2 instance container backend port 5001 & 5002).
  - **Gambar 3.3:** `03_vm2_docker_ps_2_instances_running.png` (Status container backend-node-1 dan backend-node-2 berjalan aktif).
  - **Gambar 3.4:** `04_vm2_nginx_loadbalancer_upstream_conf.png` (Konfigurasi blok upstream Nginx Load Balancer).
  - **Gambar 3.5:** `05_vm2_nginx_service_active.png` (Status service Nginx Load Balancer aktif).

### BAB 4: Konfigurasi VM 3 (Database Server & Persistent Storage)
* Gunakan folder `04_VM3_Database_Persistent_Storage/`:
  - **Gambar 4.1:** `01_vm3_ip_statis_enp0s8.png` (Alamat IP Statis 192.168.56.103).
  - **Gambar 4.2:** `02_vm3_docker_compose_mysql.png` (Konfigurasi Docker Compose MySQL 8 dan persistent volume).
  - **Gambar 4.3:** `03_vm3_docker_ps_mysql_running.png` (Container mysql-database berjalan aktif di port 3306).
  - **Gambar 4.4:** `04_vm3_docker_volume_persistent.png` (Bukti fisik Docker Named Volume `lost_found_mysql_data`).
  - **Gambar 4.5:** `05_vm3_mysql_query_select_items.png` (Bukti data barang tersimpan di database MySQL).

### BAB 5: Pengujian Sistem (Load Balancing, Failover & API)
* Gunakan folder `05_Pengujian_LoadBalancing_dan_Failover/`:
  - **Gambar 5.1:** `01_uji_konektivitas_ping_3_vm.png` (Pengujian ping inter-VM & host).
  - **Gambar 5.2:** `02_uji_load_balancing_round_robin_curl.png` (Bukti pembagian request bergantian 50:50 antara node 1 dan node 2).
  - **Gambar 5.3:** `03_uji_failover_simulasi_node1_down.png` (Bukti saat node 1 mati, traffic dialihkan 100% ke node 2 tanpa downtime).
  - **Gambar 5.4:** `04_uji_failover_recovery_node1.png` (Bukti saat node 1 pulih, request kembali seimbang).
  - **Gambar 5.5:** `05_uji_rest_api_json_response.png` (Bukti respon JSON REST API dengan metadata `served_by`).

### LAMPIRAN: Setup Awal VirtualBox
* Gunakan folder `06_Arsip_Instalasi_VirtualBox/` jika dosen menginginkan rekam jejak instalasi ISO Ubuntu Server awal.
