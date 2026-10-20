-- ========================================================
-- Database Initialization Script: Campus Lost & Found
-- Mata Kuliah: Cloud Computing
-- ========================================================

CREATE DATABASE IF NOT EXISTS `lost_found_db`
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `lost_found_db`;

-- Drop table if exists for clean migration
DROP TABLE IF EXISTS `items`;

-- Create Table Items
CREATE TABLE `items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(150) NOT NULL,
    `type` ENUM('lost', 'found') NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `description` TEXT NOT NULL,
    `location` VARCHAR(150) NOT NULL,
    `date_event` DATE NOT NULL,
    `contact_name` VARCHAR(100) NOT NULL,
    `contact_phone` VARCHAR(25) NOT NULL,
    `status` ENUM('open', 'resolved') NOT NULL DEFAULT 'open',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed Data (Data Awal untuk Pengujian)
INSERT INTO `items` (`title`, `type`, `category`, `description`, `location`, `date_event`, `contact_name`, `contact_phone`, `status`) VALUES
('KTM Universitas Trunojoyo Madura An. Dimas Prasetyo', 'lost', 'Dokumen/KTM', 'KTM hilang bersama dompet coklat kulit. Ada stiker hologram UTM.', 'Gedung RKB Lt 2', '2026-10-07', 'Dimas Prasetyo', '081234567890', 'open'),
('Kunci Motor Honda Vario dengan Gantungan Karakter Doraemon', 'found', 'Kendaraan/Kunci', 'Ditemukan tergantung di stop kontak gazebo dekat perpustakaan pusat.', 'Gazebo Depan Perpustakaan', '2026-10-08', 'Siti Rahma', '082198765432', 'open'),
('Earphone Bluetooth TWS Hitam Baseus', 'found', 'Elektronik', 'Tertinggal di meja paling belakang Lab Komputer C.', 'Lab Komputer C', '2026-10-08', 'Laboran Lab', '085712345678', 'open'),
('Jaket Hoodie Abu-abu Kampus SI UTM', 'lost', 'Pakaian/Aksesoris', 'Lupa ditaruh di kursi kantin teknik saat jam istirahat siang.', 'Kantin Fakultas Teknik', '2026-10-06', 'Rian Hidayat', '081345678912', 'resolved');
