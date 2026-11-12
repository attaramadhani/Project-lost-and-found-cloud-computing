# -*- coding: utf-8 -*-
"""
Master Generator Panduan Teknis & SOP Terpisah untuk Seluruh Tahap Live Demo:
1. Tahap 1 & 6: Attala Alif Ramadhani Tri Hida (230441100144) - Cloud Infra & Pembukaan/Penutup
2. Tahap 2: Tanji (230441100045) - Database Server MySQL & Persistent Storage
3. Tahap 4: Muhammad Naufal Widiatmoko (230441100125) - Nginx Load Balancer Round-Robin
4. Tahap 5: Moh. Yoga Dwi Prasetyo (240441100133) - Web SPA, CRUD & Failover Chaos Test
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'<w:{edge} {nsdecls("w")} w:val="{edge_data.get("val", "single")}" w:sz="{edge_data.get("sz", 4)}" w:space="0" w:color="{edge_data.get("color", "auto")}"/>'
            tcBorders.append(parse_xml(tag))
        else:
            tag = f'<w:{edge} {nsdecls("w")} w:val="none"/>'
            tcBorders.append(parse_xml(tag))
    tcPr.append(tcBorders)

class StageDocBuilder:
    def __init__(self, header_title, footer_title):
        self.doc = Document()
        for section in self.doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)
            section.page_width = Inches(8.5)
            section.page_height = Inches(11.0)
            section.different_first_page_header_footer = True

            header = section.header
            hp = header.paragraphs[0]
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            hrun = hp.add_run(header_title)
            hrun.font.name = 'Calibri'
            hrun.font.size = Pt(8.5)
            hrun.font.color.rgb = RGBColor(148, 163, 184)

            footer = section.footer
            fp = footer.paragraphs[0]
            fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            frun = fp.add_run(footer_title)
            frun.font.name = 'Calibri'
            frun.font.size = Pt(8.5)
            frun.font.color.rgb = RGBColor(148, 163, 184)

        self.COLOR_PRIMARY = RGBColor(30, 58, 138)    # #1E3A8A - UTM Dark Navy
        self.COLOR_SECONDARY = RGBColor(37, 99, 235)  # #2563EB - Royal Blue
        self.COLOR_DARK = RGBColor(15, 23, 42)        # #0F172A - Slate 900
        self.COLOR_MUTED = RGBColor(71, 85, 105)      # #475569 - Slate 600
        self.COLOR_GREEN = RGBColor(22, 101, 52)      # #166534 - Forest Green
        self.COLOR_AMBER = RGBColor(180, 83, 9)       # #B45309 - Amber Dark

        normal_style = self.doc.styles['Normal']
        normal_style.font.name = 'Calibri'
        normal_style.font.size = Pt(11)
        normal_style.font.color.rgb = self.COLOR_DARK
        normal_style.paragraph_format.line_spacing = 1.15
        normal_style.paragraph_format.space_after = Pt(4)

    def add_h1(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_PRIMARY
        return p

    def add_h2(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_SECONDARY
        return p

    def add_h3(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_DARK
        return p

    def add_lead_paragraph(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        run = p.add_run(text)
        run.font.size = Pt(10.5)
        run.font.color.rgb = self.COLOR_DARK
        return p

    def add_callout(self, title, text, callout_type="info"):
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)

        cell = tbl.cell(0, 0)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=150)

        border_color = "1E3A8A"
        bg_color = "EFF6FF"
        title_color = self.COLOR_PRIMARY

        if callout_type == "warning":
            border_color = "D97706"
            bg_color = "FFFBEB"
            title_color = self.COLOR_AMBER
        elif callout_type == "success":
            border_color = "16A34A"
            bg_color = "F0FDF4"
            title_color = self.COLOR_GREEN

        set_cell_background(cell, bg_color)
        set_cell_border(cell,
            left={"val": "single", "sz": 24, "color": border_color},
            top={"val": "single", "sz": 4, "color": "E2E8F0"},
            right={"val": "single", "sz": 4, "color": "E2E8F0"},
            bottom={"val": "single", "sz": 4, "color": "E2E8F0"}
        )

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"📌 {title.upper()}\n")
        r_title.bold = True
        r_title.font.size = Pt(10)
        r_title.font.color.rgb = title_color

        r_text = p.add_run(text)
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = self.COLOR_DARK

        self.doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_dialogue_box(self, speaker, role, dialogue_text):
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)

        cell = tbl.cell(0, 0)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=150)
        set_cell_background(cell, "F8FAFC")
        set_cell_border(cell,
            left={"val": "single", "sz": 28, "color": "2563EB"},
            top={"val": "single", "sz": 4, "color": "E2E8F0"},
            right={"val": "single", "sz": 4, "color": "E2E8F0"},
            bottom={"val": "single", "sz": 4, "color": "E2E8F0"}
        )

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)

        r_speaker = p.add_run(f"🎙️ SCRIPT BICARA PRESENTER: {speaker.upper()} ({role})\n")
        r_speaker.bold = True
        r_speaker.font.size = Pt(10)
        r_speaker.font.color.rgb = self.COLOR_SECONDARY

        r_text = p.add_run(f'"{dialogue_text}"')
        r_text.italic = True
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = self.COLOR_DARK

        self.doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_code_block(self, title, command_str, explanation=None, expected_output=None):
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)

        cell = tbl.cell(0, 0)
        set_cell_margins(cell, top=110, bottom=110, left=140, right=120)
        set_cell_background(cell, "0F172A")
        set_cell_border(cell,
            left={"val": "single", "sz": 8, "color": "334155"},
            top={"val": "single", "sz": 8, "color": "334155"},
            right={"val": "single", "sz": 8, "color": "334155"},
            bottom={"val": "single", "sz": 8, "color": "334155"}
        )

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        if title:
            r_title = p.add_run(f"# PERINTAH: {title}\n")
            r_title.bold = True
            r_title.font.name = 'Consolas'
            r_title.font.size = Pt(8.5)
            r_title.font.color.rgb = RGBColor(148, 163, 184)

        if explanation:
            r_exp = p.add_run(f"# FUNGSI: {explanation}\n")
            r_exp.font.name = 'Consolas'
            r_exp.font.size = Pt(8)
            r_exp.font.italic = True
            r_exp.font.color.rgb = RGBColor(148, 163, 184)

        r_cmd = p.add_run(f"$ {command_str}\n" if not command_str.startswith("#") else f"{command_str}\n")
        r_cmd.bold = True
        r_cmd.font.name = 'Consolas'
        r_cmd.font.size = Pt(9)
        r_cmd.font.color.rgb = RGBColor(56, 189, 248)

        if expected_output:
            r_out_lbl = p.add_run("# Output Terminal yang Diharapkan:\n")
            r_out_lbl.font.name = 'Consolas'
            r_out_lbl.font.size = Pt(8)
            r_out_lbl.font.color.rgb = RGBColor(148, 163, 184)

            r_out = p.add_run(f"{expected_output}\n")
            r_out.font.name = 'Consolas'
            r_out.font.size = Pt(8.5)
            r_out.font.color.rgb = RGBColor(241, 245, 249)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_styled_table(self, headers, data, col_widths=None):
        tbl = self.doc.add_table(rows=len(data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        hdr_row = tbl.rows[0]
        trPr = hdr_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for idx, header_text in enumerate(headers):
            cell = hdr_row.cells[idx]
            if col_widths and idx < len(col_widths):
                cell.width = Inches(col_widths[idx])
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
            set_cell_border(cell,
                top={"val": "single", "sz": 6, "color": "1E3A8A"},
                bottom={"val": "single", "sz": 12, "color": "2563EB"},
                left={"val": "single", "sz": 4, "color": "3B82F6"},
                right={"val": "single", "sz": 4, "color": "3B82F6"}
            )
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(header_text)
            run.bold = True
            run.font.name = 'Calibri'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, row_data in enumerate(data):
            row = tbl.rows[r_idx + 1]
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                if col_widths and c_idx < len(col_widths):
                    cell.width = Inches(col_widths[c_idx])
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                set_cell_border(cell,
                    top={"val": "single", "sz": 4, "color": "E2E8F0"},
                    bottom={"val": "single", "sz": 4, "color": "E2E8F0"},
                    left={"val": "single", "sz": 4, "color": "E2E8F0"},
                    right={"val": "single", "sz": 4, "color": "E2E8F0"}
                )
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(str(val))
                run.font.name = 'Calibri'
                run.font.size = Pt(9)
                run.font.color.rgb = self.COLOR_DARK

        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image_with_caption(self, img_path, caption, width=Inches(5.6)):
        if os.path.exists(img_path):
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(5)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=width)

            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(6)
            run_cap = p_cap.add_run(f"Gambar: {caption}")
            run_cap.font.name = 'Calibri'
            run_cap.font.size = Pt(8.5)
            run_cap.font.italic = True
            run_cap.font.color.rgb = self.COLOR_MUTED
        else:
            p_warn = self.doc.add_paragraph(f"[Gambar tidak ditemukan di: {img_path}]")
            p_warn.paragraph_format.space_after = Pt(4)

    def add_cover(self, title_text, subtitle_text, presenter_name, nim, role_text, extra_profile=None):
        p_cov_top = self.doc.add_paragraph()
        p_cov_top.paragraph_format.space_before = Pt(16)
        p_cov_top.paragraph_format.space_after = Pt(8)
        p_cov_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_univ = p_cov_top.add_run("UNIVERSITAS TRUNOJOYO MADURA\nFAKULTAS TEKNIK — PROGRAM STUDI S1 SISTEM INFORMASI\n")
        r_univ.bold = True
        r_univ.font.size = Pt(12)
        r_univ.font.color.rgb = self.COLOR_PRIMARY

        r_div = p_cov_top.add_run("━" * 45 + "\n")
        r_div.font.color.rgb = self.COLOR_SECONDARY

        p_title = self.doc.add_paragraph()
        p_title.paragraph_format.space_before = Pt(10)
        p_title.paragraph_format.space_after = Pt(6)
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_title = p_title.add_run(title_text + "\n")
        r_title.bold = True
        r_title.font.size = Pt(16)
        r_title.font.color.rgb = self.COLOR_PRIMARY

        p_sub = self.doc.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(14)
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_sub = p_sub.add_run(f"\"{subtitle_text}\"")
        r_sub.italic = True
        r_sub.font.size = Pt(10)
        r_sub.font.color.rgb = self.COLOR_MUTED

        p_dosen = self.doc.add_paragraph()
        p_dosen.paragraph_format.space_before = Pt(4)
        p_dosen.paragraph_format.space_after = Pt(8)
        p_dosen.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_dosen = p_dosen.add_run("Dosen Pengampu:\n")
        r_dosen.font.size = Pt(10.5)
        r_dosen_name = p_dosen.add_run("Firmansyah Adiputra, S.T., M.Sc.\n")
        r_dosen_name.bold = True
        r_dosen_name.font.size = Pt(11.5)
        r_dosen_name.font.color.rgb = self.COLOR_PRIMARY

        profil_headers = ["Informasi Penanggung Jawab", "Detail Teknis"]
        profil_data = [
            ["Nama Mahasiswa", presenter_name],
            ["Nomor Induk Mahasiswa (NIM)", nim],
            ["Peran Tim (Role)", role_text],
        ]
        if extra_profile:
            profil_data.extend(extra_profile)

        self.add_styled_table(profil_headers, profil_data, [2.5, 4.0])

        p_foot_cov = self.doc.add_paragraph()
        p_foot_cov.paragraph_format.space_before = Pt(12)
        p_foot_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_foot = p_foot_cov.add_run("BANGKALAN — JAWA TIMUR\nTAHUN AKADEMIK 2024/2025")
        r_foot.bold = True
        r_foot.font.size = Pt(10)
        r_foot.font.color.rgb = self.COLOR_PRIMARY

        self.doc.add_page_break()

    def save(self, filepath):
        self.doc.save(filepath)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"Generated: {filepath} ({size_kb:.2f} KB)")


# =============================================================================
# 1. GENERATE TAHAP 1 & 6 (ATTALA ALIF RAMADHANI TRI HIDA)
# =============================================================================
def generate_tahap1_and_6():
    b = StageDocBuilder(
        "Panduan SOP Tahap 1 & 6: Cloud Infrastructure Lead — Cloud Computing UTM",
        "Penanggung Jawab: Attala Alif Ramadhani Tri Hida (230441100144) | Dosen: Firmansyah Adiputra, S.T., M.Sc."
    )

    b.add_cover(
        "PANDUAN LENGKAP & STANDAR OPERASIONAL (SOP)\nTAHAP 1 & TAHAP 6: CLOUD INFRASTRUCTURE,\nPEMBUKAAN TOPOLOGI MULTI-VM, & PENUTUP",
        "Buku Panduan Eksekusi Live Demo: Pembukaan, Verifikasi Jaringan Multi-VM VirtualBox Subnet 192.168.56.0/24, Koordinasi Estafet Tim, Evaluasi Rubrik, dan Shutdown Terpusat",
        "Attala Alif Ramadhani Tri Hida",
        "230441100144",
        "Ketua Kelompok & Cloud Infrastructure Lead",
        [
            ["Target Virtual Machine", "VM1 (192.168.56.101), VM2 (192.168.56.102), VM3 (192.168.56.103)"],
            ["Tugas Pokok Tahap 1", "Pembukaan, Penjelasan Topologi 3-VM, Uji Ping Multi-VM sekaligus"],
            ["Tugas Pokok Tahap 6", "Rangkuman Ketercapaian Rubrik Nilai A, Sesi Tanya Jawab, Penutup"],
        ]
    )

    # Bab 1
    b.add_h1("BAB 1: LANDASAN TEORI & ARSITEKTUR CLOUD VIRTUALISASI")
    b.add_h2("1.1 Mengapa Memilih Type-2 Hypervisor (VirtualBox)?")
    b.add_lead_paragraph(
        "Dalam mata kuliah Cloud Computing, mahasiswa diajarkan dua jenis arsitektur virtualisasi: "
        "Type-1 (Bare-Metal seperti VMware ESXi/Proxmox) dan Type-2 (Hosted Hypervisor seperti VirtualBox). "
        "Karena lingkungan pengujian menggunakan satu perangkat laptop fisik mahasiswa tanpa menghapus sistem operasi utama (Windows 11), "
        "Type-2 Hypervisor adalah solusi paling efisien dan tepat guna untuk mensimulasikan data center cloud lokal."
    )
    b.add_h2("1.2 Rationale Pemilihan Host-Only Ethernet Adapter")
    b.add_lead_paragraph(
        "Banyak mahasiswa keliru memilih mode NAT atau Bridged. Berikut alasan teknis mengapa Host-Only Network (192.168.56.0/24) adalah pilihan mutlak:"
    )
    b.add_lead_paragraph(
        "1. Isolasi & Keamanan: Subnet Host-Only sepenuhnya privat. Server tidak terpapar bahaya flooding atau sniffing dari jaringan Wi-Fi publik kampus.\n"
        "2. Deterministic Static IP: IP ketiga VM (.101, .102, .103) diikat permanen melalui Netplan YAML. Jika menggunakan Bridged, IP akan berubah-ubah setiap laptop connect ke hotspot Wi-Fi yang berbeda, merusak konfigurasi upstream Load Balancer dan DB connection string."
    )
    b.add_image_with_caption(
        "screenshots/01_Arsitektur_dan_Ketentuan/03_diagram_topologi_deployment_multi_vm.png",
        "Topologi Jaringan Deployment Multi-VM VirtualBox pada Subnet Host-Only 192.168.56.0/24"
    )

    # Bab 2
    b.add_h1("BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (PRE-FLIGHT)")
    b.add_h2("2.1 Prosedur Penyalaan Mesin Virtual (Cold-Boot Order)")
    b.add_lead_paragraph(
        "Sebagai Ketua Tim dan Infra Lead, Anda memegang kendali atas penyalaan ketiga VM. Patuhi urutan wajib:"
    )
    b.add_lead_paragraph(
        "1. Start VM3-Database (.103) -> Tunggu 30 detik hingga MySQL port 3306 ready.\n"
        "2. Start VM2-Backend (.102) -> Tunggu 20 detik hingga Docker backend 5001/5002 Up.\n"
        "3. Start VM1-Frontend (.101) -> Nginx melayani file statis SPA React."
    )
    b.add_code_block(
        "Skrip PowerShell Menyalakan 3 VM Sekaligus Secara Headless",
        '"VM3-Database", "VM2-Backend", "VM1-Frontend" | ForEach-Object { & "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe" startvm $_ --type headless }',
        "Menjalankan ketiga VM di latar belakang tanpa jendela GUI terpisah yang membebani layar.",
        "Waiting for VM \"VM3-Database\" to power on...\nVM \"VM3-Database\" has been successfully started."
    )
    b.add_callout(
        "JIKA MUNCUL ERROR 'ALREADY LOCKED BY A SESSION'",
        "Itu artinya VM Anda SUDAH MENYALA di background atau di UI VirtualBox Manager. Jangan di-start ulang! "
        "Langsung lakukan Test-Connection untuk memverifikasi responnya.",
        callout_type="warning"
    )

    # Bab 3
    b.add_h1("BAB 3: ALUR KERJA KESELURUHAN & MANAJEMEN ESTAFET TIM")
    b.add_lead_paragraph(
        "Sebagai Ketua Kelompok, Anda bertindak sebagai konduktor orkestra presentasi. "
        "Berikut alur pembagian waktu 15 menit live demo:"
    )
    al_h = ["Menit Ke-", "Tahap Demo", "Presenter", "Fokus Aksi di Layar"]
    al_d = [
        ["00:00 - 02:00", "Tahap 1", "Attala Alif (ANDA)", "Buka presentasi, sapa dosen, jelaskan topologi, uji Test-Connection 3 VM."],
        ["02:00 - 05:00", "Tahap 2", "Tanji", "SSH ke VM3, docker ps, docker volume ls, query SELECT items."],
        ["05:00 - 08:00", "Tahap 3", "Naufal Husain", "SSH ke VM2, cat docker-compose.yml, docker ps 2 instance, curl port 5001 & 5002."],
        ["08:00 - 11:00", "Tahap 4", "M. Naufal Widiatmoko", "Cat nginx-lb.conf, jelaskan upstream Round-Robin, loop PowerShell 6x (50:50)."],
        ["11:00 - 14:00", "Tahap 5", "Moh. Yoga Dwi", "Demo Web SPA, CRUD laporan baru, DUET CHAOS FAILOVER TEST."],
        ["14:00 - 15:00", "Tahap 6", "Attala Alif (ANDA)", "Tegaskan 100% rubrik terpenuhi, buka sesi tanya jawab, penutup."],
    ]
    b.add_styled_table(al_h, al_d, [1.2, 0.9, 1.8, 2.6])

    # Bab 4
    b.add_h1("BAB 4: PELAKSANAAN DEMO TAHAP 1 (PEMBUKAAN & UJI MULTI-VM)")
    b.add_dialogue_box(
        "Attala Alif Ramadhani Tri Hida",
        "Ketua Tim & Cloud Infra Lead",
        "Selamat pagi/siang Pak Firman dan rekan-rekan. Kami dari Kelompok Proyek Cloud Computing akan mendemonstrasikan sistem "
        "'Campus Lost & Found' berbasis Multi-VM Hypervisor Type-2 Oracle VirtualBox. "
        "Pada proyek ini, kami memecah aplikasi menjadi 3 Virtual Machine terisolasi di subnet Host-Only 192.168.56.0/24: "
        "VM 1 untuk Frontend SPA React, VM 2 untuk Backend Cluster dan Load Balancer Nginx, serta VM 3 untuk Database MySQL Persisten. "
        "Sebagai langkah awal, saya akan membuktikan bahwa ketiga VM ini benar-benar aktif mandiri dan saling terhubung dengan latensi 0 ms."
    )
    b.add_h2("Langkah 1: Menampilkan Dashboard VirtualBox Manager")
    b.add_lead_paragraph(
        "Tunjukkan jendela VirtualBox Manager di mana VM1-Frontend, VM2-Backend, dan VM3-Database berstatus hijau (Running)."
    )
    b.add_h2("Langkah 2: Eksekusi Uji Multi-VM Ping Sekaligus")
    b.add_code_block(
        "Uji Ping 3 VM Sekaligus di PowerShell Host",
        "Test-Connection -ComputerName 192.168.56.101, 192.168.56.102, 192.168.56.103 -Count 1",
        "Mengirim paket ICMP Echo Request ke ketiga VM secara paralel dari komputer Host Windows.",
        "Source        Destination     IPV4Address      Bytes    Time(ms)\n"
        "------        -----------     -----------      -----    --------\n"
        "MSI-LAPTOP    192.168.56.101  192.168.56.101   32       0 (VM1 UP)\n"
        "MSI-LAPTOP    192.168.56.102  192.168.56.102   32       0 (VM2 UP)\n"
        "MSI-LAPTOP    192.168.56.103  192.168.56.103   32       0 (VM3 UP)"
    )
    b.add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/01_uji_konektivitas_ping_3_vm.png",
        "Bukti Uji Konektivitas Multi-VM Host-Only dengan Latensi 0 ms"
    )
    b.add_h2("Langkah 3: Menyerahkan Estafet ke Tahap 2")
    b.add_dialogue_box(
        "Attala Alif Ramadhani Tri Hida",
        "Ketua Tim",
        "Seluruh node virtual telah terbukti aktif dan terhubung. Selanjutnya, rekan saya Tanji akan mendemonstrasikan "
        "infrastruktur basis data pada VM 3, pembuktian kontainer Docker MySQL 8, dan mekanisme Persistent Volume. Silakan Mas Tanji."
    )

    # Bab 5
    b.add_h1("BAB 5: PELAKSANAAN DEMO TAHAP 6 (KESIMPULAN & PENUTUP)")
    b.add_dialogue_box(
        "Attala Alif Ramadhani Tri Hida",
        "Ketua Tim",
        "Terima kasih Mas Yoga. Pak Firman dan rekan-rekan, dari seluruh rangkaian pengujian tadi, kami telah membuktikan "
        "kepatuhan 100% terhadap seluruh rubrik penilaian Cloud Computing:\n"
        "1. Arsitektur Multi-VM Type-2 VirtualBox terpisah di 3 VM independen.\n"
        "2. Frontend SPA React ter-compile production dan disajikan oleh Nginx di VM 1.\n"
        "3. Backend cluster minimal 2 instance kontainer Docker (port 5001 & 5002) di VM 2.\n"
        "4. Load Balancer Round-Robin 50:50 dan Zero-Downtime Failover di VM 2.\n"
        "5. Database MySQL 8 di VM 3 dengan Docker Persistent Volume anti hilang.\n"
        "Demikian demonstrasi dari kelompok kami. Waktu dan tempat kami persilakan kepada Pak Firman untuk sesi tanya jawab."
    )

    # Bab 6
    b.add_h1("BAB 6: PANDUAN TANYA JAWAB KRITIS (Q&A DEFENSE GUIDE) KHUSUS INFRASTRUCTURE")
    qa_infra = [
        ("Q1: Apa kelemahan Type-2 Hypervisor dibanding Type-1 di dunia nyata?",
         "\"Type-2 Hypervisor memiliki overhead performa karena instruksi hardware harus melewati Host OS (Windows) sebelum dieksekusi CPU, "
         "sehingga ada latensi sekitar 5-10%. Untuk data center enterprise skala besar, Type-1 (Bare Metal) lebih disukai karena langsung berbicara ke hardware. "
         "Namun untuk tahap development, testing, dan simulasi multi-server di laptop mahasiswa, Type-2 adalah yang paling efisien tanpa merusak OS utama.\""),
        ("Q2: Berapa total alokasi RAM yang Anda gunakan untuk 3 VM ini?",
         "\"Total RAM yang dialokasikan adalah 5.0 GB dari total 16 GB RAM laptop fisik kami: 1.5 GB untuk VM1 Frontend, 2.0 GB untuk VM2 Backend Cluster, "
         "dan 1.5 GB untuk VM3 Database. Alokasi ini sangat hemat karena seluruh VM menggunakan Ubuntu Server tanpa GUI (headless).\""),
        ("Q3: Mengapa menggunakan Netplan statis bukan DHCP dari VirtualBox?",
         "\"DHCP Server VirtualBox berpotensi memberikan dynamic IP yang berubah saat VM reboot. Karena konfigurasi Nginx Load Balancer mengarah ke IP statis "
         "192.168.56.102 dan Database di 192.168.56.103, kami menonaktifkan DHCP dan mengunci IP secara statis via file /etc/netplan/01-static-netcfg.yaml.\"")
    ]
    for q_t, q_a in qa_infra:
        b.add_h2(q_t)
        b.add_callout("KUNCI JAWABAN ATTALA ALIF", q_a, callout_type="success")

    # Bab 7
    b.add_h1("BAB 7: PROSEDUR SHUTDOWN BERSIH KESELURUHAN (CLEAN SHUTDOWN)")
    b.add_lead_paragraph(
        "Setelah ujian selesai, jalankan skrip graceful shutdown satu baris ini di PowerShell Host:"
    )
    b.add_code_block(
        "ACPI Poweroff Terpusat dari PowerShell Host",
        '"VM1-Frontend", "VM2-Backend", "VM3-Database" | ForEach-Object { & "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe" controlvm $_ acpipowerbutton }',
        "Mengirim sinyal ACPI shutdown resmi ke kernel ketiga VM secara berurutan tanpa risiko kerusakan disk."
    )
    b.save("PANDUAN_TEKNIS_TAHAP_1_DAN_6_CLOUD_INFRASTRUCTURE_ATTALA.docx")


# =============================================================================
# 2. GENERATE TAHAP 2 (TANJI - DATABASE & PERSISTENT STORAGE)
# =============================================================================
def generate_tahap2():
    b = StageDocBuilder(
        "Panduan SOP Tahap 2: Database & Persistent Storage — Cloud Computing UTM",
        "Penanggung Jawab: Tanji (230441100045) | Dosen: Firmansyah Adiputra, S.T., M.Sc."
    )

    b.add_cover(
        "PANDUAN LENGKAP & STANDAR OPERASIONAL (SOP)\nTAHAP 2: PEMBUKTIAN DATABASE SERVER MYSQL 8\n& DOCKER PERSISTENT VOLUME STORAGE",
        "Buku Panduan Eksekusi Live Demo: Pembuktian Kontainer MySQL di VM 3 Terpisah, Verifikasi Fisik Docker Named Volume Anti-Hilang, Isolasi Keamanan Akses, dan Eksekusi Query SQL Langsung",
        "Tanji",
        "230441100045",
        "Database & Frontend Deployment Specialist",
        [
            ["Target Virtual Machine", "VM3-Database (Alamat IP: 192.168.56.103)"],
            ["Layanan Utama", "Docker Engine, MySQL 8.0 Container (Port 3306)"],
            ["Penyimpanan Persisten", "Docker Named Volume: lost_found_mysql_data -> /var/lib/mysql"],
            ["Tugas Pokok Tahap 2", "Membuktikan database terpisah, volume persisten, dan query SELECT"],
        ]
    )

    # Bab 1
    b.add_h1("BAB 1: LANDASAN TEORI & ARSITEKTUR BASIS DATA CLOUD")
    b.add_h2("1.1 Mengapa Database Wajib Ditempatkan di VM Terpisah?")
    b.add_lead_paragraph(
        "Dalam prinsip Cloud Computing Decoupled Architecture, basis data adalah lapisan stateful yang paling bernilai. "
        "Menyatukan database dengan server aplikasi (backend) dalam 1 VM adalah praktik buruk karena lonjakan beban komputasi API "
        "dapat menyita CPU/RAM database, serta meningkatkan risiko keamanan jika server backend disusupi hacker. "
        "Dengan memisahkan database ke VM 3 (192.168.56.103), kita menerapkan isolasi keamanan jaringan dan alokasi resource independen."
    )
    b.add_h2("1.2 Konsep Docker Named Volume: Menjamin Data Anti-Hilang")
    b.add_lead_paragraph(
        "Secara default, kontainer Docker bersifat 'ephemeral' (data di layer kontainer akan musnah saat kontainer dihentikan atau dihapus). "
        "Untuk mencegah data laporan barang kampus lenyap, kita menggunakan Docker Named Volume 'lost_found_mysql_data'. "
        "Volume ini memetakan folder data InnoDB (/var/lib/mysql) langsung ke filesystem disk fisik VM 3 (/var/lib/docker/volumes/...). "
        "Meskipun kontainer MySQL mengalami crash, stop, atau di-recreate, data tetap aman tersimpan di disk."
    )
    b.add_image_with_caption(
        "screenshots/04_VM3_Database_Persistent_Storage/04_vm3_docker_volume_persistent.png",
        "Bukti Fisik Docker Named Volume 'lost_found_mysql_data' di VM 3"
    )

    # Bab 2
    b.add_h1("BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (PRE-FLIGHT)")
    b.add_h2("2.1 Prosedur Menjalankan Database Pertama Kali")
    b.add_code_block(
        "Inisialisasi Container MySQL di VM 3",
        "ssh atta@192.168.56.103\ncd ~/database\ndocker compose up -d",
        "Mengangkat kontainer mysql-database dan me-mount volume lost_found_mysql_data.",
        "[+] Running 2/2\n"
        " ✔ Network database_default            Created\n"
        " ✔ Container mysql-database           Started"
    )
    b.add_h2("2.2 Checklist Kesiapan Sebelum Giliran Presentasi")
    chk_h = ["No", "Parameter Kesiapan", "Perintah Cepat di VM3", "Kondisi Lolos (PASS)"]
    chk_d = [
        ["1", "Status MySQL Container", "docker ps", "Status 'Up' di port 0.0.0.0:3306->3306/tcp"],
        ["2", "Status Volume Persisten", "docker volume ls", "Menampilkan volume 'lost_found_mysql_data'"],
        ["3", "Koneksi Socket MySQL", "docker exec -it mysql-database mysqladmin ping -u root -prahasia123", "mysqld is alive"],
    ]
    b.add_styled_table(chk_h, chk_d, [0.4, 2.0, 2.5, 1.6])

    # Bab 3
    b.add_h1("BAB 3: ALUR ESTAFET & TITIK SERAH TERIMA")
    b.add_callout(
        "TITIK MASUK DARI ATTALA (TAHAP 1)",
        "Attala akan menutup: '...Selanjutnya rekan saya Tanji akan mendemonstrasikan infrastruktur basis data di VM 3. Silakan Mas Tanji.'\n"
        "👉 Segera mulai dengan script pembuka Anda!",
        callout_type="info"
    )

    # Bab 4
    b.add_h1("BAB 4: PELAKSANAAN DEMO TAHAP 2 LANGKAH DEMI LANGKAH")
    b.add_dialogue_box(
        "Tanji",
        "Database Specialist",
        "Terima kasih Attala. Selanjutnya saya Tanji akan mendemonstrasikan implementasi pada VM 3 dengan alamat IP 192.168.56.103. "
        "Sesuai ketentuan Pak Firman, database wajib dideploy pada VM yang berbeda sebagai container Docker dan memiliki persistent storage. "
        "Di sini saya telah menyiapkan kontainer MySQL 8 dengan nama 'mysql-database' yang terikat pada Docker Named Volume 'lost_found_mysql_data'. "
        "Dengan arsitektur ini, sekalipun kontainer dihentikan atau dihapus, data laporan barang kampus tidak akan hilang. "
        "Mari kita buktikan status kontainer, volume fisik, dan isi tabel datanya secara langsung di terminal VM 3."
    )
    b.add_h2("Langkah 1: Remote Login SSH ke VM 3")
    b.add_code_block("Koneksi SSH ke VM 3", "ssh atta@192.168.56.103", "Password: 12345. Membuka terminal Ubuntu Server VM 3.")
    b.add_h2("Langkah 2: Tampilkan IP Statis VM 3")
    b.add_code_block("Verifikasi Alamat IP VM 3", "ip a show enp0s8", "Membuktikan terminal berada pada IP statis 192.168.56.103.")
    b.add_h2("Langkah 3: Tampilkan Status Kontainer Docker MySQL")
    b.add_code_block("Cek Kontainer MySQL Berjalan", "docker ps", "Menunjukkan kontainer mysql-database Up di port 3306.")
    b.add_image_with_caption(
        "screenshots/04_VM3_Database_Persistent_Storage/03_vm3_docker_ps_mysql_running.png",
        "Status Kontainer MySQL 8 Berjalan Aktif pada Port 3306 di VM 3"
    )
    b.add_h2("Langkah 4: Buktikan Docker Persistent Volume Fisik")
    b.add_code_block(
        "Verifikasi Volume Docker",
        "docker volume ls && docker volume inspect lost_found_mysql_data",
        "Menampilkan daftar volume dan mountpoint fisik /var/lib/docker/volumes/lost_found_mysql_data/_data."
    )
    b.add_h2("Langkah 5: Eksekusi Query Langsung ke Dalam MySQL Container")
    b.add_code_block(
        "Query Menampilkan Data Barang dari Database",
        "docker exec -it mysql-database mysql -u root -prahasia123 lost_found_db -e \"SELECT id, title, category, status FROM items;\"",
        "Mengeksekusi SQL langsung di dalam kontainer tanpa perlu menginstal mysql-client di host VM.",
        "+----+---------------------------+----------------+----------+\n"
        "| id | title                     | category       | status   |\n"
        "+----+---------------------------+----------------+----------+\n"
        "|  1 | KTM an. Budi Santoso      | Dokumen / KTM  | lost     |\n"
        "|  2 | Kunci Motor Honda Vario   | Kendaraan      | found    |\n"
        "|  3 | Earphone TWS Anker Hitam  | Elektronik     | found    |\n"
        "|  4 | Jaket Hoodie Hitam Polos  | Pakaian        | resolved |\n"
        "+----+---------------------------+----------------+----------+"
    )
    b.add_image_with_caption(
        "screenshots/04_VM3_Database_Persistent_Storage/05_vm3_mysql_query_select_items.png",
        "Bukti Query Data Barang dari Database MySQL Tersimpan Lengkap"
    )
    b.add_h2("Langkah 6: Serahkan Estafet ke Naufal Husain (Tahap 3)")
    b.add_dialogue_box(
        "Tanji",
        "Database Specialist",
        "Database MySQL di VM 3 telah terbukti aktif, terisolasi, dan aman dengan persistent volume. "
        "Selanjutnya, untuk pembuktian minimal 2 instance backend application server di VM 2, "
        "saya serahkan kepada rekan saya Naufal Husain. Silakan Mas Naufal."
    )

    # Bab 5
    b.add_h1("BAB 5: PERAN DUKUNGAN SAAT TAHAP 5 (VERIFIKASI CRUD YOGA)")
    b.add_lead_paragraph(
        "Saat Mas Moh. Yoga Dwi menginput barang baru di browser host pada Tahap 5, "
        "NILAI PLUS BESAR BAGI TANJI adalah menjalankan kembali query SQL untuk membuktikan data baru tersebut langsung masuk:"
    )
    b.add_code_block(
        "Verifikasi Real-Time Data Masuk dari Web ke MySQL VM 3",
        "docker exec -it mysql-database mysql -u root -prahasia123 lost_found_db -e \"SELECT id, title, contact_name FROM items ORDER BY id DESC LIMIT 1;\"",
        "Membuktikan aliran data End-to-End dari Browser -> VM1 -> VM2 -> VM3 sukses 100%!"
    )

    # Bab 6
    b.add_h1("BAB 6: PANDUAN TANYA JAWAB KRITIS (Q&A DEFENSE GUIDE) KHUSUS DATABASE")
    qa_db = [
        ("Q1: Mengapa tidak memakai bind mount (-v /host/path:/var/lib/mysql) tapi named volume?",
         "\"Named Volume dikelola langsung oleh Docker Engine (/var/lib/docker/volumes) sehingga memiliki manajemen permission yang aman "
         "dan performa I/O optimal tanpa terbentur masalah UID/GID filesystem Linux host.\""),
        ("Q2: Apa yang terjadi jika kontainer MySQL di-restart saat ada transaksi?",
         "\"Engine MySQL kami menggunakan InnoDB dengan konfigurasi ACID compliant. InnoDB memiliki mekanisme redo log dan transaction journal "
         "sehingga jika terjadi crash mendadak, engine akan melakukan auto-recovery saat menyala kembali tanpa merusak integritas tabel.\""),
        ("Q3: Bagaimana keamanan akses database di VM 3 dijaga?",
         "\"Port 3306 hanya dibuka di subnet privat Host-Only 192.168.56.0/24 khusus melayani koneksi REST API dari VM 2, sehingga tidak "
         "dapat diakses langsung dari jaringan publik maupun dari layer Frontend VM 1.\"")
    ]
    for q_t, q_a in qa_db:
        b.add_h2(q_t)
        b.add_callout("KUNCI JAWABAN TANJI", q_a, callout_type="success")

    b.save("PANDUAN_TEKNIS_TAHAP_2_DATABASE_PERSISTENT_STORAGE_TANJI.docx")


# =============================================================================
# 3. GENERATE TAHAP 4 (M. NAUFAL WIDIATMOKO - LOAD BALANCER)
# =============================================================================
def generate_tahap4():
    b = StageDocBuilder(
        "Panduan SOP Tahap 4: Nginx Load Balancer Round-Robin — Cloud Computing UTM",
        "Penanggung Jawab: Muhammad Naufal Widiatmoko (230441100125) | Dosen: Firmansyah Adiputra, S.T., M.Sc."
    )

    b.add_cover(
        "PANDUAN LENGKAP & STANDAR OPERASIONAL (SOP)\nTAHAP 4: PEMBUKTIAN NGINX LOAD BALANCER\nROUND-ROBIN & HIGH AVAILABILITY REVERSE PROXY",
        "Buku Panduan Eksekusi Live Demo: Pembedahan Blok Upstream Nginx Port 80, Distribusi Beban Seimbang 50:50, Pengujian Loop PowerShell, dan Konfigurasi Failover Timeout",
        "Muhammad Naufal Widiatmoko",
        "230441100125",
        "Load Balancer & Reverse Proxy Engineer",
        [
            ["Target Virtual Machine", "VM2-Backend (Alamat IP: 192.168.56.102:80)"],
            ["Layanan Utama", "Nginx Reverse Proxy & Load Balancer Engine"],
            ["Algoritma Load Balancing", "Round-Robin Standar (Port 5001 & Port 5002)"],
            ["Mekanisme Failover", "proxy_next_upstream error timeout http_500 http_502 http_503"],
        ]
    )

    # Bab 1
    b.add_h1("BAB 1: LANDASAN TEORI & ARSITEKTUR LOAD BALANCING")
    b.add_h2("1.1 Mengapa Membutuhkan Load Balancer di Depan Backend Cluster?")
    b.add_lead_paragraph(
        "Pada Tahap 3, Naufal Husain telah membuktikan adanya 2 instance backend di port 5001 dan port 5002. "
        "Namun, aplikasi klien (browser frontend) tidak boleh dibebani logika memilih server mana yang harus dihubungi. "
        "Klien membutuhkan Single Point of Access. Nginx dipasang di port 80 VM 2 sebagai pintu gerbang tunggal (Reverse Proxy) "
        "yang secara transparan membagi request masuk ke kedua backend tersebut secara seimbang (Round-Robin)."
    )
    b.add_h2("1.2 Cara Kerja Algoritma Round-Robin & Failover Timeout")
    b.add_lead_paragraph(
        "1. Pembagian Beban Bergantian: Request #1 diteruskan ke 127.0.0.1:5001, Request #2 ke 127.0.0.1:5002, Request #3 ke 5001, dan seterusnya secara seimbang 50:50.\n"
        "2. Health Check Pasif: Dengan parameter 'max_fails=2 fail_timeout=5s', jika satu backend gagal merespons 2 kali, Nginx menandai node tersebut inaktif selama 5 detik.\n"
        "3. Zero Downtime: Dengan klausul 'proxy_next_upstream', kegagalan koneksi di node pertama langsung diputar ke node kedua dalam hitungan milidetik."
    )
    b.add_image_with_caption(
        "screenshots/03_VM2_Backend_Cluster_LoadBalancer/04_vm2_nginx_loadbalancer_upstream_conf.png",
        "Blok Konfigurasi Upstream dan Reverse Proxy Nginx Load Balancer di VM 2"
    )

    # Bab 2
    b.add_h1("BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (PRE-FLIGHT)")
    b.add_code_block(
        "Uji Validitas Konfigurasi Nginx di VM 2",
        "sudo nginx -t && sudo systemctl status nginx",
        "Memastikan sintaks konfigurasi /etc/nginx/sites-available/default valid (syntax is ok) dan servis active.",
        "nginx: the configuration file /etc/nginx/nginx.conf syntax is ok\n"
        "nginx: configuration file /etc/nginx/nginx.conf test is successful\n"
        "● nginx.service - A high performance web server and a reverse proxy server\n"
        "     Active: active (running)"
    )

    # Bab 3
    b.add_h1("BAB 3: ALUR ESTAFET & TITIK SERAH TERIMA")
    b.add_callout(
        "TITIK MASUK DARI NAUFAL HUSAIN (TAHAP 3)",
        "Naufal Husain akan menutup: '...Selanjutnya rekan saya Muhammad Naufal Widiatmoko akan mendemonstrasikan Nginx Load Balancer di port 80. Silakan Mas Widiatmoko.'\n"
        "👉 Langsung sambut dengan script bicara Anda!",
        callout_type="info"
    )

    # Bab 4
    b.add_h1("BAB 4: PELAKSANAAN DEMO TAHAP 4 LANGKAH DEMI LANGKAH")
    b.add_dialogue_box(
        "Muhammad Naufal Widiatmoko",
        "Load Balancer Engineer",
        "Terima kasih Naufal Husain. Karena terdapat dua kontainer backend yang berjalan di VM 2, kami membutuhkan pintu gerbang tunggal "
        "yang membagi beban kerja secara seimbang ke kedua kontainer tersebut. Di sini saya mengonfigurasikan Nginx sebagai Reverse Proxy "
        "dan Load Balancer di Port 80 VM 2. Nginx menggunakan blok upstream 'backend_servers' dengan algoritma Round-Robin. "
        "Setiap request yang masuk akan didistribusikan bergantian 50:50 ke port 5001 dan port 5002. "
        "Mari kita lihat berkas konfigurasinya dan kita uji pembagian bebannya secara live melalui loop cURL dari Host."
    )
    b.add_h2("Langkah 1: Menampilkan Konfigurasi Upstream Nginx")
    b.add_code_block(
        "Bedah Konfigurasi Upstream Nginx",
        "cat /etc/nginx/sites-available/default | grep -A 14 'upstream backend_servers'",
        "Menunjukkan bukti kode konfigurasi Round-Robin dan failover Nginx.",
        "upstream backend_servers {\n"
        "    server 127.0.0.1:5001 max_fails=2 fail_timeout=5s;\n"
        "    server 127.0.0.1:5002 max_fails=2 fail_timeout=5s;\n"
        "}\n"
        "server {\n"
        "    listen 80 default_server;\n"
        "    location / {\n"
        "        proxy_pass http://backend_servers;\n"
        "        proxy_connect_timeout 2s;\n"
        "        proxy_next_upstream error timeout http_500 http_502 http_503;\n"
        "    }\n"
        "}"
    )
    b.add_h2("Langkah 2: Uji Pembagian Beban Round-Robin 6 Kali Loop")
    b.add_lead_paragraph(
        "Beralih ke jendela PowerShell Host Windows, jalankan loop request berikut:"
    )
    b.add_code_block(
        "Loop Request HTTP ke IP VM 2 dari Host Windows",
        "for ($i=1; $i -le 6; $i++) { (Invoke-RestMethod -Uri 'http://192.168.56.102/api/health').served_by }",
        "Mengirim 6 request berturut-turut ke port 80 VM 2 untuk melihat distribusi respon node.",
        "backend-node-1\n"
        "backend-node-2\n"
        "backend-node-1\n"
        "backend-node-2\n"
        "backend-node-1\n"
        "backend-node-2"
    )
    b.add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/02_uji_load_balancing_round_robin_curl.png",
        "Bukti Distribusi Beban Round-Robin Bergantian Sempurna 50:50 Antar Kontainer"
    )
    b.add_h2("Langkah 3: Menyerahkan Estafet ke Moh. Yoga Dwi (Tahap 5)")
    b.add_dialogue_box(
        "Muhammad Naufal Widiatmoko",
        "Load Balancer Engineer",
        "Distribusi beban Round-Robin telah terbukti bekerja 50:50 secara presisi. Selanjutnya rekan saya Moh. Yoga Dwi Prasetyo "
        "akan mendemonstrasikan antarmuka web SPA, pengujian CRUD end-to-end, serta pengujian ketahanan failover saat salah satu node dimatikan. Silakan Mas Yoga."
    )

    # Bab 5
    b.add_h1("BAB 5: PANDUAN TANYA JAWAB KRITIS (Q&A DEFENSE GUIDE) KHUSUS LOAD BALANCER")
    qa_lb = [
        ("Q1: Apa bedanya algoritma Round-Robin, Least Connections, dan IP Hash?",
         "\"Round-Robin membagi request bergantian berurutan secara merata (cocok untuk server spesifikasi seimbang). "
         "Least Connections mengarahkan request ke server yang sedang melayani koneksi aktif paling sedikit (cocok untuk request durasi panjang). "
         "IP Hash mengikat IP klien ke satu server tertentu untuk mempertahankan session state.\""),
        ("Q2: Mengapa header CORS tidak ditambahkan dua kali di Nginx dan Express?",
         "\"Jika Nginx menambahkan header 'Access-Control-Allow-Origin: *' dan Express juga menambahkannya, browser akan menerima duplikasi "
         "header '* , *' yang menyebabkan browser memblokir request karena melanggar CORS standard RFC. Oleh karena itu, kami menyerahkan CORS "
         "sepenuhnya ke Express middleware dan Nginx murni bertindak sebagai reverse proxy transparan.\""),
        ("Q3: Apa fungsi parameter proxy_next_upstream?",
         "\"Parameter ini adalah kunci High Availability. Ketika Nginx mencoba meneruskan koneksi ke node 1 dan node tersebut down (error/timeout), "
         "Nginx tidak mengembalikan HTTP 502 Bad Gateway ke pengguna, melainkan secara cerdas langsung mengulang request yang sama ke node 2.\"")
    ]
    for q_t, q_a in qa_lb:
        b.add_h2(q_t)
        b.add_callout("KUNCI JAWABAN WIDIATMOKO", q_a, callout_type="success")

    b.save("PANDUAN_TEKNIS_TAHAP_4_LOAD_BALANCER_ROUND_ROBIN_WIDIATMOKO.docx")


# =============================================================================
# 4. GENERATE TAHAP 5 (MOH. YOGA DWI PRASETYO - WEB SPA & FAILOVER)
# =============================================================================
def generate_tahap5():
    b = StageDocBuilder(
        "Panduan SOP Tahap 5: Web SPA, CRUD & Chaos Failover — Cloud Computing UTM",
        "Penanggung Jawab: Moh. Yoga Dwi Prasetyo (240441100133) | Dosen: Firmansyah Adiputra, S.T., M.Sc."
    )

    b.add_cover(
        "PANDUAN LENGKAP & STANDAR OPERASIONAL (SOP)\nTAHAP 5: DEMONSTRASI WEB SPA REACT 18,\nUJI CRUD END-TO-END, & SIMULASI CHAOS FAILOVER TEST",
        "Buku Panduan Eksekusi Live Demo: Pembuktian Web SPA di VM 1 (192.168.56.101), Pengujian Aliran Data Penuh (CRUD), Simulasi Server Crash (docker stop backend-node-1), Bukti Zero-Downtime Failover, dan Pemulihan Otomatis (Auto-Recovery)",
        "Moh. Yoga Dwi Prasetyo",
        "240441100133",
        "QA, Stress Testing & Documentation Lead",
        [
            ["Target Virtual Machine", "VM1-Frontend (192.168.56.101) & Host Browser"],
            ["Teknologi Antarmuka", "Single Page Application React 18 + Vite + Tailwind CSS"],
            ["Pengujian Utama 1", "Uji Aliran Data Lengkap (CRUD): Input Laporan -> Simpan di MySQL VM3"],
            ["Pengujian Utama 2 (POIN A ⭐)", "Simulasi Server Crash & Zero-Downtime Failover (Node 1 Stop)"],
        ]
    )

    # Bab 1
    b.add_h1("BAB 1: LANDASAN TEORI & ARSITEKTUR FRONTEND PRODUCTION")
    b.add_h2("1.1 Mengapa Frontend Berupa Single Page Application (SPA)?")
    b.add_lead_paragraph(
        "Sesuai ketentuan dosen pengampu, antarmuka pengguna wajib berupa Single Page Application (SPA). "
        "Aplikasi SPA React memuat seluruh shell aplikasi dalam satu kali pemuatan halaman. "
        "Navigasi tab filter barang hilang/temuan, pencarian real-time, dan pengiriman formulir berlangsung mulus "
        "tanpa reload halaman browser (zero page reloads), memberikan user experience yang sangat responsif layaknya aplikasi mobile modern."
    )
    b.add_h2("1.2 Mengapa Disajikan Melalui Nginx Production Build di VM 1?")
    b.add_lead_paragraph(
        "Kode React 18 dikompilasi ke static bundle HTML, JS, dan CSS menggunakan 'npm run build', lalu disalin ke direktori "
        "/var/www/html pada VM 1 (192.168.56.101). Nginx bertindak sebagai web server statis berkecepatan tinggi yang hanya "
        "mengonsumsi sedikit RAM (< 30 MB), memenuhi standar industri produksi cloud sesungguhnya."
    )
    b.add_image_with_caption(
        "screenshots/02_VM1_Frontend_SPA/04_browser_portal_lost_and_found_home.png",
        "Antarmuka Single Page Application (SPA) Portal Campus Lost & Found pada Browser Host"
    )

    # Bab 2
    b.add_h1("BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (PRE-FLIGHT)")
    b.add_code_block(
        "Buka Tab Browser di Komputer Host Sebelum Maju",
        "Buka Google Chrome / Edge: http://192.168.56.101",
        "Pastikan halaman web Lost & Found muncul sempurna, daftar barang terload dari API, dan status Nginx di VM 1 active."
    )

    # Bab 3
    b.add_h1("BAB 3: ALUR ESTAFET & TITIK SERAH TERIMA")
    b.add_callout(
        "TITIK MASUK DARI WIDIATMOKO (TAHAP 4)",
        "Widiatmoko akan menutup: '...Selanjutnya rekan saya Moh. Yoga Dwi Prasetyo akan mendemonstrasikan antarmuka web SPA, "
        "uji CRUD, serta pengujian failover. Silakan Mas Yoga.'\n"
        "👉 Segera ambil alih dengan percaya diri!",
        callout_type="info"
    )

    # Bab 4
    b.add_h1("BAB 4: PELAKSANAAN DEMO TAHAP 5 LANGKAH DEMI LANGKAH")
    b.add_dialogue_box(
        "Moh. Yoga Dwi Prasetyo",
        "QA & Testing Lead",
        "Terima kasih Mas Widiatmoko. Sekarang kita masuk ke pengujian fungsional aplikasi dan uji ketahanan sistem (Chaos Test). "
        "Pertama, saya membuka browser di komputer host ke alamat http://192.168.56.101. Halaman ini disajikan oleh Nginx di VM 1 "
        "dari build statis React 18. Antarmuka memiliki fitur filter instan, pencarian, dan integrasi WhatsApp. "
        "Sekarang saya akan melakukan uji aliran data penuh (CRUD End-to-End), lalu kita lakukan pengujian paling krusial, "
        "yaitu Failover Test dengan mematikan paksa salah satu kontainer backend."
    )

    b.add_h2("Pengujian 5A: Demonstrasi Web SPA & Uji CRUD End-to-End")
    b.add_lead_paragraph(
        "1. Di browser host (http://192.168.56.101), klik tombol '+ Lapor Barang Baru'.\n"
        "2. Masukkan data uji nyata: Judul 'KTM Sistem Informasi an. Yoga Dwi', Kategori 'Dokumen / KTM', Lokasi 'Lab CBT FT UTM', Kontak WA '08123456789'.\n"
        "3. Klik 'Simpan Laporan' -> Data langsung muncul seketika di kartu layar tanpa reload halaman browser.\n"
        "4. Mas Tanji di VM 3 mengeksekusi query SELECT di MySQL membuktikan data langsung tersimpan secara permanen!"
    )
    b.add_image_with_caption(
        "screenshots/02_VM1_Frontend_SPA/05_browser_form_lapor_barang_baru.png",
        "Formulir Pelaporan Barang Baru yang Terhubung Secara End-to-End ke Backend & Database"
    )

    b.add_h2("Pengujian 5B: UJI FAILOVER / CHAOS TEST (POIN NILAI A ⭐)")
    b.add_lead_paragraph(
        "Ini adalah pembuktian ilmiah paling penting bagi Dosen Penguji:"
    )
    b.add_dialogue_box(
        "Moh. Yoga Dwi Prasetyo",
        "QA & Testing Lead",
        "Sekarang mari kita buktikan ketahanan sistem jika terjadi kegagalan server backend. "
        "Saya meminta rekan saya Mas Naufal Husain di terminal VM 2 untuk mematikan paksa kontainer backend-node-1 sekarang juga."
    )
    b.add_lead_paragraph(
        "1. Naufal Husain mengeksekusi: 'docker stop backend-node-1' di VM 2.\n"
        "2. Di PowerShell Host, Yoga menjalankan loop curl:"
    )
    b.add_code_block(
        "Loop Request Saat backend-node-1 Mati",
        "for ($i=1; $i -le 4; $i++) { (Invoke-RestMethod -Uri 'http://192.168.56.102/api/health').served_by }",
        "Membuktikan 100% request langsung dialihkan ke node 2 tanpa error 502 Bad Gateway.",
        "backend-node-2\n"
        "backend-node-2\n"
        "backend-node-2\n"
        "backend-node-2\n"
        "# BUKTI: Zero Downtime! Tidak ada request yang gagal!"
    )
    b.add_lead_paragraph(
        "3. Yoga me-refresh browser host: Website TETAP BERJALAN NORMAL dan tidak crash!\n"
        "4. Yoga memberi aba-aba: 'Sekarang Mas Naufal tolong nyalakan kembali backend-node-1.'\n"
        "5. Naufal mengeksekusi: 'docker start backend-node-1' di VM 2.\n"
        "6. Yoga menjalankan loop curl lagi: Nginx otomatis mendeteksi node yang telah pulih dan membagi beban seimbang 50:50 kembali!"
    )
    b.add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/03_uji_failover_simulasi_node1_down.png",
        "Bukti Zero-Downtime Failover: Traffic Otomatis Dialihkan 100% ke backend-node-2"
    )
    b.add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/04_uji_failover_recovery_node1.png",
        "Bukti Auto-Recovery: Permintaan Kembali Seimbang Begitu Node 1 Dinyalakan"
    )

    b.add_h2("Langkah 3: Serahkan Estafet ke Attala Alif (Tahap 6)")
    b.add_dialogue_box(
        "Moh. Yoga Dwi Prasetyo",
        "QA Lead",
        "Demikian pengujian antarmuka web SPA, pengujian CRUD end-to-end, dan pembuktian failover tanpa downtime. "
        "Selanjutnya untuk penutupan dan rangkuman penilaian, saya kembalikan kepada Ketua Kelompok Attala Alif. Terima kasih."
    )

    # Bab 5
    b.add_h1("BAB 5: PANDUAN TANYA JAWAB KRITIS (Q&A DEFENSE GUIDE) KHUSUS TESTING")
    qa_qa = [
        ("Q1: Bagaimana Anda mengukur performa atau waktu respon saat terjadi failover?",
         "\"Kami mengukur menggunakan time measurement PowerShell. Saat node 1 mati, request mengalami penundaan sesaat (sekitar 200 ms) "
         "karena Nginx menunggu fail_timeout sebelum mengalihkan soket ke node 2. Namun klien di browser sama sekali tidak menerima HTTP status 502/500, "
         "sehingga dari sisi user experience (UX) ketersediaan sistem tetap 100%.\""),
        ("Q2: Mengapa tombol WhatsApp di setiap kartu barang penting dalam arsitektur cloud ini?",
         "\"Fitur ini mengintegrasikan protokol eksternal wa.me secara instan dengan metadata barang yang diambil dari REST API backend. "
         "Ketika tombol diklik, klien langsung diarahkan ke nomor kontak pelapor yang divalidasi oleh database di VM 3.\"")
    ]
    for q_t, q_a in qa_qa:
        b.add_h2(q_t)
        b.add_callout("KUNCI JAWABAN YOGA DWI", q_a, callout_type="success")

    b.save("PANDUAN_TEKNIS_TAHAP_5_WEB_SPA_CRUD_DAN_CHAOS_FAILOVER_YOGA.docx")


if __name__ == "__main__":
    print("Membangun semua dokumen panduan teknis per tahap...")
    generate_tahap1_and_6()
    generate_tahap2()
    generate_tahap4()
    generate_tahap5()
    print("Semua dokumen Word berhasil dibuat!")
