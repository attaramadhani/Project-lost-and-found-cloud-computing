# -*- coding: utf-8 -*-
"""
Generator Laporan Panduan & Skenario Live Demo Final Project Cloud Computing
Universitas Trunojoyo Madura - Dosen Pengampu: Firmansyah Adiputra, S.T., M.Sc.
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
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for table cells in dxa (1 pt = 20 dxa)."""
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
    """
    Set cell borders: top, bottom, left, right.
    kwargs: e.g. left={"sz": 24, "val": "single", "color": "1E3A8A"}
    """
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

def create_document():
    doc = Document()

    # 1. Page Margins (1 inch / 2.54 cm all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Configure different first page header/footer
        section.different_first_page_header_footer = True
        
        # Normal Header (Page 2 onwards)
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Panduan Live Demo Final Project Cloud Computing — S1 Sistem Informasi UTM")
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)

        # Normal Footer (Page 2 onwards)
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Campus Lost & Found Architecture (Multi-VM Type-2 Hypervisor) | Dosen: Firmansyah Adiputra, S.T., M.Sc.")
        frun.font.name = 'Calibri'
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Styling constants
    COLOR_PRIMARY = RGBColor(30, 58, 138)    # #1E3A8A - UTM Dark Navy
    COLOR_SECONDARY = RGBColor(37, 99, 235)  # #2563EB - Royal Blue
    COLOR_DARK = RGBColor(15, 23, 42)        # #0F172A - Slate 900
    COLOR_MUTED = RGBColor(71, 85, 105)      # #475569 - Slate 600
    COLOR_GREEN = RGBColor(22, 101, 52)      # #166534 - Forest Green
    COLOR_AMBER = RGBColor(180, 83, 9)       # #B45309 - Amber Dark

    # Default paragraph format
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_DARK
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Helper functions
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_DARK
        return p

    def add_lead_paragraph(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        run = p.add_run(text)
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_callout(title, text, callout_type="info"):
        """Callout box with colored left border."""
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)

        cell = tbl.cell(0, 0)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=150)

        border_color = "1E3A8A"
        bg_color = "EFF6FF"
        title_color = COLOR_PRIMARY

        if callout_type == "warning":
            border_color = "D97706"
            bg_color = "FFFBEB"
            title_color = COLOR_AMBER
        elif callout_type == "success":
            border_color = "16A34A"
            bg_color = "F0FDF4"
            title_color = COLOR_GREEN

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
        r_text.font.color.rgb = COLOR_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_dialogue_box(speaker, role, dialogue_text):
        """Spoken dialogue script box for presenters."""
        tbl = doc.add_table(rows=1, cols=1)
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
        r_speaker.font.color.rgb = COLOR_SECONDARY

        r_text = p.add_run(f'"{dialogue_text}"')
        r_text.italic = True
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = COLOR_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_code_block(title, command_str, expected_output=None):
        """Code block showing commands and expected terminal output."""
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)

        cell = tbl.cell(0, 0)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=120)
        set_cell_background(cell, "0F172A") # Dark terminal background
        set_cell_border(cell,
            left={"val": "single", "sz": 8, "color": "334155"},
            top={"val": "single", "sz": 8, "color": "334155"},
            right={"val": "single", "sz": 8, "color": "334155"},
            bottom={"val": "single", "sz": 8, "color": "334155"}
        )

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        if title:
            r_title = p.add_run(f"# {title}\n")
            r_title.bold = True
            r_title.font.name = 'Consolas'
            r_title.font.size = Pt(8.5)
            r_title.font.color.rgb = RGBColor(148, 163, 184) # Light Slate

        r_cmd = p.add_run(f"$ {command_str}\n" if not command_str.startswith("#") else f"{command_str}\n")
        r_cmd.bold = True
        r_cmd.font.name = 'Consolas'
        r_cmd.font.size = Pt(9)
        r_cmd.font.color.rgb = RGBColor(56, 189, 248) # Cyan terminal text

        if expected_output:
            r_out_lbl = p.add_run("# Output yang Diharapkan:\n")
            r_out_lbl.font.name = 'Consolas'
            r_out_lbl.font.size = Pt(8)
            r_out_lbl.font.color.rgb = RGBColor(148, 163, 184)

            r_out = p.add_run(f"{expected_output}\n")
            r_out.font.name = 'Consolas'
            r_out.font.size = Pt(8.5)
            r_out.font.color.rgb = RGBColor(241, 245, 249) # Near white

        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_styled_table(headers, data, col_widths=None):
        """Generate a sleek, academic styled table with Navy header and zebra stripes."""
        tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        # Header Row
        hdr_row = tbl.rows[0]
        trPr = hdr_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for idx, header_text in enumerate(headers):
            cell = hdr_row.cells[idx]
            if col_widths and idx < len(col_widths):
                cell.width = Inches(col_widths[idx])
            set_cell_background(cell, "1E3A8A") # Navy Blue
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

        # Data Rows
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
                run.font.color.rgb = COLOR_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image_with_caption(img_path, caption, width=Inches(5.6)):
        """Add image centered with bold italic caption."""
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(5)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(6)
            run_cap = p_cap.add_run(f"Gambar: {caption}")
            run_cap.font.name = 'Calibri'
            run_cap.font.size = Pt(8.5)
            run_cap.font.italic = True
            run_cap.font.color.rgb = COLOR_MUTED
        else:
            p_warn = doc.add_paragraph(f"[Gambar tidak ditemukan di: {img_path}]")
            p_warn.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # HALAMAN COVER / JUDUL RESMI
    # =========================================================================
    p_cov_top = doc.add_paragraph()
    p_cov_top.paragraph_format.space_before = Pt(20)
    p_cov_top.paragraph_format.space_after = Pt(8)
    p_cov_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_univ = p_cov_top.add_run("UNIVERSITAS TRUNOJOYO MADURA\nFAKULTAS TEKNIK — PROGRAM STUDI S1 SISTEM INFORMASI\n")
    r_univ.bold = True
    r_univ.font.size = Pt(12)
    r_univ.font.color.rgb = COLOR_PRIMARY

    r_div = p_cov_top.add_run("━" * 45 + "\n")
    r_div.font.color.rgb = COLOR_SECONDARY

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("LAPORAN PANDUAN DAN SKENARIO LIVE DEMO\nFINAL PROJECT CLOUD COMPUTING\n")
    r_title.bold = True
    r_title.font.size = Pt(17)
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(
        "\"Implementasi Sistem Campus Lost & Found Menggunakan Multi-VM VirtualBox Hypervisor Type-2, "
        "Cluster Backend Multi-Instance Docker, Nginx Load Balancer Round-Robin & Failover, "
        "serta Database MySQL dengan Persistent Volume Storage\""
    )
    r_sub.italic = True
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = COLOR_MUTED

    p_dosen = doc.add_paragraph()
    p_dosen.paragraph_format.space_before = Pt(6)
    p_dosen.paragraph_format.space_after = Pt(10)
    p_dosen.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dosen = p_dosen.add_run("Dosen Pengampu:\n")
    r_dosen.font.size = Pt(10.5)
    r_dosen_name = p_dosen.add_run("Firmansyah Adiputra, S.T., M.Sc.\n")
    r_dosen_name.bold = True
    r_dosen_name.font.size = Pt(11.5)
    r_dosen_name.font.color.rgb = COLOR_PRIMARY

    # Team Members Table on Cover
    members_headers = ["No", "Nama Mahasiswa", "NIM", "Peran / Tanggung Jawab Utama"]
    members_data = [
        ["1", "Attala Alif Ramadhani Tri Hida", "230441100144", "Ketua Kelompok & Cloud Infrastructure Lead"],
        ["2", "Tanji", "230441100045", "Database & Frontend Deployment Specialist"],
        ["3", "Naufal Husain", "240441100038", "Backend & Containerization Specialist"],
        ["4", "Muhammad Naufal Widiatmoko", "230441100125", "Load Balancer & Reverse Proxy Engineer"],
        ["5", "Moh. Yoga Dwi Prasetyo", "240441100133", "QA, Stress Testing & Documentation Lead"],
    ]
    add_styled_table(members_headers, members_data, [0.4, 2.3, 1.3, 2.5])

    p_foot_cov = doc.add_paragraph()
    p_foot_cov.paragraph_format.space_before = Pt(16)
    p_foot_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot_cov.add_run("BANGKALAN — JAWA TIMUR\nTAHUN AKADEMIK 2024/2025")
    r_foot.bold = True
    r_foot.font.size = Pt(10.5)
    r_foot.font.color.rgb = COLOR_PRIMARY

    doc.add_page_break()

    # =========================================================================
    # BAB 1: IKHTISAR SISTEM & TOPOLOGI CLOUD COMPUTING
    # =========================================================================
    add_h1("BAB 1: IKHTISAR SISTEM & ARSITEKTUR CLOUD COMPUTING")

    add_h2("1.1 Latar Belakang Proyek")
    add_lead_paragraph(
        "Proyek ini dibangun sebagai luaran tugas akhir mata kuliah Cloud Computing pada Program Studi S1 Sistem Informasi "
        "Universitas Trunojoyo Madura. Sistem yang diimplementasikan adalah 'Campus Lost & Found', sebuah portal pelaporan "
        "dan pencarian barang hilang atau ditemukan di lingkungan sivitas akademika kampus. "
        "Aplikasi dirancang mengikuti standar arsitektur cloud terdistribusi (multi-tier decoupling) untuk menjamin "
        "ketersediaan tinggi (High Availability), skalabilitas beban (Load Balancing), serta keamanan data persisten."
    )

    add_h2("1.2 Kepatuhan Terhadap Ketentuan Penugasan Dosen")
    add_lead_paragraph(
        "Seluruh komponen infrastruktur dan aplikasi 100% mematuhi instruksi resmi dari dosen pengampu (Firmansyah Adiputra, S.T., M.Sc.) "
        "sebagaimana dirangkum dalam matriks kepatuhan berikut:"
    )

    rubrik_headers = ["Ketentuan Dosen", "Implementasi Nyata Tim", "Status Verifikasi"]
    rubrik_data = [
        ["Hypervisor Mandiri di Laptop", "Oracle VM VirtualBox (Type-2 Hypervisor) di atas Host Windows 11", "100% Terpenuhi"],
        ["Multi-VM (Tiap Layanan 1 VM)", "3 VM Ubuntu Server terpisah (VM1: Frontend, VM2: Backend, VM3: Database)", "100% Terpenuhi"],
        ["Frontend Single Page Application (SPA)", "Aplikasi React 18 + Vite + Tailwind CSS dibuild production ke VM1", "100% Terpenuhi"],
        ["Minimal 2 Instance Application Server", "Docker Compose menjalankan 2 kontainer backend Express.js (Port 5001 & 5002)", "100% Terpenuhi"],
        ["Load Balancer untuk Distribusi Beban", "Nginx Load Balancer Reverse Proxy (Port 80) algoritma Round-Robin & Failover", "100% Terpenuhi"],
        ["Database di VM Berbeda & Persistent", "MySQL 8 Container di VM 3 terpisah dengan Docker Named Volume", "100% Terpenuhi"],
        ["Peran Jelas Tiap Anggota Kelompok", "5 Anggota memiliki pembagian tugas teknis dan bagian presentasi masing-masing", "100% Terpenuhi"],
    ]
    add_styled_table(rubrik_headers, rubrik_data, [2.0, 3.2, 1.3])

    add_image_with_caption(
        "screenshots/01_Arsitektur_dan_Ketentuan/01_ketentuan_deployment_slide_kuliah.png",
        "Slide Ketentuan Resmi Deployment Multi-VM Mata Kuliah Cloud Computing"
    )

    add_h2("1.3 Spesifikasi Lingkungan Host & Virtualisasi")
    add_lead_paragraph(
        "Sistem dijalankan secara lokal di atas satu mesin fisik (Physical Laptop Host) tanpa ketergantungan pada koneksi "
        "cloud publik berbayar. Seluruh komunikasi antar-VM difasilitasi oleh VirtualBox Host-Only Ethernet Adapter "
        "pada subnet lokal 192.168.56.0/24."
    )

    spec_headers = ["Komponen", "Spesifikasi Fisik Laptop", "Alokasi Virtualisasi"]
    spec_data = [
        ["Processor (CPU)", "Intel Core i7-13620H (10 Cores, 16 Threads)", "1 vCPU dialokasikan per masing-masing VM"],
        ["Memory (RAM)", "16 GB DDR5 5200 MHz", "Total 5.0 GB (VM1: 1.5 GB, VM2: 2.0 GB, VM3: 1.5 GB)"],
        ["Storage (Disk)", "SSD NVMe PCIe Gen4 1 TB", "20 GB Dynamically Allocated per VM (Ubuntu LVM)"],
        ["Sistem Operasi Host", "Microsoft Windows 11 Home 64-bit", "Host Hypervisor Platform"],
        ["Hypervisor", "Oracle VM VirtualBox Versi 7.0.x", "Type-2 Hosted Hypervisor"],
        ["Virtual Network", "VirtualBox Host-Only Ethernet Adapter", "Gateway Host: 192.168.56.1 (Subnet 255.255.255.0)"],
    ]
    add_styled_table(spec_headers, spec_data, [1.8, 2.5, 2.2])

    add_h2("1.4 Matriks Rincian 3 Virtual Machine (Multi-VM Architecture)")
    vm_headers = ["Identitas VM", "Hostname & IP Statis", "Layanan / Software", "Port Aktif", "Resource"]
    vm_data = [
        ["VM 1: Frontend", "vm1-frontend\n192.168.56.101", "Nginx Web Server\nReact 18 SPA (Build)", "Port 80 (HTTP)\nPort 22 (SSH)", "1 vCPU\n1.5 GB RAM"],
        ["VM 2: Backend & LB", "vm2-backend\n192.168.56.102", "Nginx Load Balancer\nDocker: backend-node-1\nDocker: backend-node-2", "Port 80 (LB Proxy)\nPort 5001 (Node 1)\nPort 5002 (Node 2)\nPort 22 (SSH)", "2 vCPU\n2.0 GB RAM"],
        ["VM 3: Database", "vm3-database\n192.168.56.103", "Docker MySQL 8.0 Engine\nVolume: lost_found_mysql_data", "Port 3306 (MySQL)\nPort 22 (SSH)", "1 vCPU\n1.5 GB RAM"],
    ]
    add_styled_table(vm_headers, vm_data, [1.2, 1.4, 1.9, 1.2, 0.8])

    add_image_with_caption(
        "screenshots/01_Arsitektur_dan_Ketentuan/02_diagram_arsitektur_aplikasi_3tier.png",
        "Diagram Logis Arsitektur Aplikasi 3-Tier (Client SPA -> Load Balancer & Cluster API -> Database Persisten)"
    )

    add_image_with_caption(
        "screenshots/01_Arsitektur_dan_Ketentuan/03_diagram_topologi_deployment_multi_vm.png",
        "Topologi Jaringan Deployment Multi-VM VirtualBox pada Subnet Host-Only 192.168.56.0/24"
    )

    doc.add_page_break()

    # =========================================================================
    # BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (PRE-FLIGHT CHECKLIST)
    # =========================================================================
    add_h1("BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (PRE-FLIGHT CHECKLIST)")

    add_lead_paragraph(
        "Sebelum kelompok dipanggil oleh Dosen Pengampu untuk melakukan live demo, Ketua dan seluruh tim wajib "
        "memastikan seluruh tahapan persiapan berikut telah selesai 100%. Kelalaian dalam urutan persiapan dapat "
        "mengakibatkan error koneksi database atau tabrakan port."
    )

    add_h2("2.1 Prosedur dan Urutan Menyalakan Virtual Machine (Cold-Boot Order)")
    add_lead_paragraph(
        "Virtual Machine TIDAK BOLEH dinyalakan secara acak. Urutan penyalaan harus mengikuti kaidah dependensi layanan backend:"
    )

    order_headers = ["Urutan", "Nama Virtual Machine", "Alasan & Ketergantungan Layanan", "Waktu Tunggu"]
    order_data = [
        ["1 (Pertama)", "VM3-Database (192.168.56.103)", "Database MySQL harus beroperasi terlebih dahulu agar saat Backend menyala, Express langsung berhasil melakukan pool connection ke port 3306.", "Tunggu ~30 detik hingga container MySQL ready."],
        ["2 (Kedua)", "VM2-Backend (192.168.56.102)", "Setelah DB hidup, nyalakan VM2 agar Docker Compose mengangkat kontainer backend-1 & 2 dan Nginx Load Balancer aktif melayani upstream.", "Tunggu ~20 detik hingga kedua kontainer Node status healthy."],
        ["3 (Ketiga)", "VM1-Frontend (192.168.56.101)", "VM1 menyajikan static files HTML/JS. Dinyalakan terakhir saat backend API sudah siap melayani request API browser.", "Tunggu ~10 detik hingga Nginx menyala."],
    ]
    add_styled_table(order_headers, order_data, [1.0, 1.8, 2.5, 1.2])

    add_callout(
        "PERHATIAN KHUSUS VIRTUALBOX RUNNING ERROR",
        "Jika di PowerShell muncul error: 'VBoxManage.exe: error: The machine is already locked by a session', "
        "itu artinya VM Anda SUDAH MENYALA di background atau di UI VirtualBox. Jangan panik! "
        "Anda cukup langsung menjalankan Test-Connection untuk memverifikasi responnya.",
        callout_type="warning"
    )

    add_h2("2.2 Verifikasi Pra-Demo di Terminal PowerShell Laptop Host")
    add_lead_paragraph(
        "Buka terminal PowerShell di Windows, lalu jalankan satu baris perintah berikut untuk membuktikan ketiga VM menyala dan terhubung:"
    )

    add_code_block(
        "Pengujian Ping Sekaligus ke 3 VM dari Host Windows",
        "Test-Connection -ComputerName 192.168.56.101, 192.168.56.102, 192.168.56.103 -Count 1",
        "Source        Destination     IPV4Address      Bytes    Time(ms)\n"
        "------        -----------     -----------      -----    --------\n"
        "MSI-LAPTOP    192.168.56.101  192.168.56.101   32       0       \n"
        "MSI-LAPTOP    192.168.56.102  192.168.56.102   32       0       \n"
        "MSI-LAPTOP    192.168.56.103  192.168.56.103   32       0       "
    )

    add_h2("2.3 Pengaturan Tata Letak Jendela Layar (Screen Layout)")
    add_lead_paragraph(
        "Agar demo terlihat sangat rapi, profesional, dan meyakinkan dosen, atur jendela pada layar laptop seperti berikut:"
    )

    screen_headers = ["Bagian Layar", "Aplikasi / Jendela", "Konten yang Ditampilkan", "Tujuan Demo"]
    screen_data = [
        ["Sisi Kiri (50% Layar)", "Google Chrome / Edge", "http://192.168.56.101 (Portal Lost & Found)", "Menunjukkan antarmuka web interaktif real-time, filter, dan form pelaporan."],
        ["Sisi Kanan Atas (25%)", "Windows Terminal (Tab 1)", "PowerShell Host: Cek ping, loop curl Round-Robin", "Membuktikan distribusi beban 50:50 secara live."],
        ["Sisi Kanan Bawah (25%)", "Windows Terminal (Tab 2 & 3)", "SSH ke VM2 (Backend) & SSH ke VM3 (Database)", "Tempat eksekusi docker stop/start (failover) dan query MySQL."],
    ]
    add_styled_table(screen_headers, screen_data, [1.4, 1.6, 2.0, 1.5])

    doc.add_page_break()

    # =========================================================================
    # BAB 3: SKENARIO & TAHAPAN LIVE DEMO LANGKAH DEMI LANGKAH
    # =========================================================================
    add_h1("BAB 3: SKENARIO & TAHAPAN LIVE DEMO LANGKAH DEMI LANGKAH")

    add_lead_paragraph(
        "Bagian ini merupakan inti pelaksanaan presentasi. Setiap anggota tim telah memiliki jatah waktu, script bicara, "
        "tindakan teknis di layar laptop, perintah terminal, serta bukti screenshot yang harus disorot ke Dosen Pengampu."
    )

    # -------------------------------------------------------------------------
    # TAHAP 1: PEMBUKAAN & UJI MULTI-VM (ATTALA)
    # -------------------------------------------------------------------------
    add_h2("TAHAP 1: Pembukaan, Ikhtisar Arsitektur & Pembuktian Multi-VM Ping (Durasi: 2 Menit)")
    add_lead_paragraph(
        "Penanggung Jawab: Attala Alif Ramadhani Tri Hida (NIM: 230441100144)\n"
        "Peran: Ketua Kelompok & Cloud Infrastructure Lead"
    )

    add_dialogue_box(
        "Attala Alif Ramadhani Tri Hida",
        "Ketua Kelompok & Cloud Infra Lead",
        "Selamat pagi/siang Pak Firman dan rekan-rekan sekalian. Kami dari Kelompok Proyek Cloud Computing akan "
        "mendemonstrasikan implementasi sistem 'Campus Lost & Found' berbasis Multi-VM Hypervisor Type-2 VirtualBox. "
        "Pada tugas ini, kami mengimplementasikan arsitektur cloud decoupling dengan memisahkan Frontend, Backend Cluster, "
        "dan Database ke dalam 3 Virtual Machine Ubuntu Server yang independen pada subnet lokal 192.168.56.0/24. "
        "Sebagai langkah awal, saya akan membuktikan bahwa ketiga VM ini benar-benar berjalan mandiri dan saling terhubung "
        "melalui Host-Only Network."
    )

    add_h3("Aksi Layar & Perintah yang Dijalankan Attala:")
    add_lead_paragraph(
        "1. Tampilkan jendela Oracle VM VirtualBox Manager yang memperlihatkan ketiga mesin: "
        "VM1-Frontend, VM2-Backend, dan VM3-Database dalam kondisi 'Running'.\n"
        "2. Buka PowerShell di Host Windows, jalankan perintah uji konektivitas 3 VM sekaligus:"
    )

    add_code_block(
        "Verifikasi Multi-VM Network di Host PowerShell",
        "Test-Connection -ComputerName 192.168.56.101, 192.168.56.102, 192.168.56.103 -Count 1",
        "Destination     IPV4Address      Bytes    Time(ms)\n"
        "-----------     -----------      -----    --------\n"
        "192.168.56.101  192.168.56.101   32       0 (VM1-Frontend UP)\n"
        "192.168.56.102  192.168.56.102   32       0 (VM2-Backend UP)\n"
        "192.168.56.103  192.168.56.103   32       0 (VM3-Database UP)"
    )

    add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/01_uji_konektivitas_ping_3_vm.png",
        "Hasil Uji Konektivitas Ping Multi-VM pada Subnet 192.168.56.0/24 (Latency 0 ms)"
    )

    # -------------------------------------------------------------------------
    # TAHAP 2: PEMBUKTIAN DATABASE SERVER & PERSISTENT STORAGE (TANJI)
    # -------------------------------------------------------------------------
    add_h2("TAHAP 2: Pembuktian Database Server MySQL & Docker Persistent Storage di VM 3 (Durasi: 3 Menit)")
    add_lead_paragraph(
        "Penanggung Jawab: Tanji (NIM: 230441100045)\n"
        "Peran: Database & Frontend Deployment Specialist"
    )

    add_dialogue_box(
        "Tanji",
        "Database Specialist",
        "Terima kasih Attala. Selanjutnya, saya akan membuktikan implementasi VM 3 pada IP 192.168.56.103. "
        "Sesuai ketentuan Pak Firman, database wajib dideploy pada VM yang berbeda sebagai container Docker dan memiliki "
        "penyimpanan persisten (Persistent Storage). Di sini saya telah menyiapkan MySQL 8.0 container dengan nama "
        "'mysql-database' yang terikat pada Docker Named Volume 'lost_found_mysql_data'. Dengan arsitektur ini, "
        "sekalipun container mengalami crash, stop, atau dihapus, seluruh data pelaporan barang kampus tidak akan hilang."
    )

    add_h3("Aksi Layar & Perintah yang Dijalankan Tanji:")
    add_lead_paragraph(
        "1. Di Terminal PowerShell Host, lakukan koneksi SSH ke VM 3:\n"
        "   Perintah: ssh atta@192.168.56.103 (Password: 12345)\n"
        "2. Tampilkan alamat IP statis VM 3 untuk membuktikan berada di mesin yang benar:\n"
        "   Perintah: ip a show enp0s8\n"
        "3. Tampilkan status kontainer Docker MySQL:\n"
        "   Perintah: docker ps\n"
        "4. Tunjukkan bukti fisik Docker Named Volume (Persistent Storage):\n"
        "   Perintah: docker volume ls\n"
        "   Perintah: docker inspect lost_found_mysql_data\n"
        "5. Eksekusi query langsung ke dalam MySQL untuk membuktikan data tersimpan:"
    )

    add_code_block(
        "Query Cek Data Barang di MySQL Container VM 3",
        "docker exec -it mysql-database mysql -u root -prahasia123 lost_found_db -e \"SELECT id, title, category, status FROM items;\"",
        "+----+---------------------------+----------------+----------+\n"
        "| id | title                     | category       | status   |\n"
        "+----+---------------------------+----------------+----------+\n"
        "|  1 | KTM an. Budi Santoso      | Dokumen / KTM  | lost     |\n"
        "|  2 | Kunci Motor Honda Vario   | Kendaraan      | found    |\n"
        "|  3 | Earphone TWS Anker Hitam  | Elektronik     | found    |\n"
        "|  4 | Jaket Hoodie Hitam Polos  | Pakaian        | resolved |\n"
        "+----+---------------------------+----------------+----------+"
    )

    add_image_with_caption(
        "screenshots/04_VM3_Database_Persistent_Storage/03_vm3_docker_ps_mysql_running.png",
        "Container MySQL 8 Berjalan Aktif pada Port 3306 di VM 3"
    )

    add_image_with_caption(
        "screenshots/04_VM3_Database_Persistent_Storage/04_vm3_docker_volume_persistent.png",
        "Bukti Docker Named Volume 'lost_found_mysql_data' Sebagai Persistent Storage"
    )

    add_image_with_caption(
        "screenshots/04_VM3_Database_Persistent_Storage/05_vm3_mysql_query_select_items.png",
        "Bukti Query Data Pelaporan Barang di Terminal VM 3 Tersimpan Lengkap"
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # TAHAP 3: PEMBUKTIAN BACKEND CLUSTER MULTI-INSTANCE (NAUFAL HUSAIN)
    # -------------------------------------------------------------------------
    add_h2("TAHAP 3: Pembuktian Backend Cluster Multi-Instance Docker di VM 2 (Durasi: 3 Menit)")
    add_lead_paragraph(
        "Penanggung Jawab: Naufal Husain (NIM: 240441100038)\n"
        "Peran: Backend & Containerization Specialist"
    )

    add_dialogue_box(
        "Naufal Husain",
        "Backend Specialist",
        "Terima kasih Mas Tanji. Pada VM 2 dengan IP 192.168.56.102, tugas saya adalah mengimplementasikan ketentuan "
        "'minimal 2 instance application server'. Untuk menghindari Single Point of Failure, aplikasi backend Express.js "
        "kami kemas dalam Dockerfile berbasis Alpine Linux dan diorkestrasi menggunakan Docker Compose menjadi dua "
        "kontainer independen, yaitu 'backend-node-1' di port 5001 dan 'backend-node-2' di port 5002. "
        "Setiap kontainer menyuntikkan environment variable APP_INSTANCE sehingga setiap request dapat mengidentifikasi "
        "secara transparan kontainer mana yang melayani."
    )

    add_h3("Aksi Layar & Perintah yang Dijalankan Naufal Husain:")
    add_lead_paragraph(
        "1. Di Terminal PowerShell Host, buka tab baru dan SSH ke VM 2:\n"
        "   Perintah: ssh atta@192.168.56.102 (Password: 12345)\n"
        "2. Tampilkan file konfigurasi orkestrasi Docker Compose:\n"
        "   Perintah: cat ~/backend/docker-compose.yml\n"
        "3. Tampilkan kedua kontainer backend yang sedang aktif:\n"
        "   Perintah: docker ps"
    )

    add_code_block(
        "Verifikasi 2 Instance Kontainer Backend di VM 2",
        "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'",
        "NAMES           STATUS         PORTS\n"
        "backend-node-1  Up 45 minutes  0.0.0.0:5001->5000/tcp\n"
        "backend-node-2  Up 45 minutes  0.0.0.0:5002->5000/tcp"
    )

    add_lead_paragraph(
        "4. Uji health check internal pada kedua instance secara terpisah:"
    )

    add_code_block(
        "Uji Respons Mandiri Tiap Instance Backend",
        "curl -s http://localhost:5001/api/health && echo '' && curl -s http://localhost:5002/api/health",
        '{"status":"UP","served_by":"backend-node-1","timestamp":"2024-..."}\n'
        '{"status":"UP","served_by":"backend-node-2","timestamp":"2024-..."}'
    )

    add_image_with_caption(
        "screenshots/03_VM2_Backend_Cluster_LoadBalancer/02_vm2_docker_compose_config.png",
        "File docker-compose.yml yang Mendefinisikan Minimal 2 Instance Backend Port 5001 & 5002"
    )

    add_image_with_caption(
        "screenshots/03_VM2_Backend_Cluster_LoadBalancer/03_vm2_docker_ps_2_instances_running.png",
        "Dua Instance Backend Berjalan Bersamaan di Port 5001 dan 5002 pada VM 2"
    )

    # -------------------------------------------------------------------------
    # TAHAP 4: PEMBUKTIAN LOAD BALANCER ROUND-ROBIN (M. NAUFAL WIDIATMOKO)
    # -------------------------------------------------------------------------
    add_h2("TAHAP 4: Pembuktian Nginx Load Balancer Round-Robin di VM 2 (Durasi: 3 Menit)")
    add_lead_paragraph(
        "Penanggung Jawab: Muhammad Naufal Widiatmoko (NIM: 230441100125)\n"
        "Peran: Load Balancer & Reverse Proxy Engineer"
    )

    add_dialogue_box(
        "Muhammad Naufal Widiatmoko",
        "Load Balancer Engineer",
        "Terima kasih Naufal Husain. Karena terdapat dua kontainer backend yang berjalan di VM 2, kami membutuhkan "
        "sebuah pintu gerbang tunggal yang membagi beban kerja secara seimbang ke kedua kontainer tersebut. "
        "Di sini saya mengonfigurasikan Nginx sebagai Reverse Proxy dan Load Balancer yang mendengarkan di Port 80 VM 2. "
        "Nginx menggunakan blok 'upstream backend_servers' dengan algoritma Round-Robin standar. "
        "Setiap request yang masuk akan didistribusikan bergantian 50:50 ke port 5001 dan port 5002. "
        "Selain itu, terdapat klausul 'proxy_next_upstream' yang menjamin pengalihan otomatis jika terjadi kegagalan."
    )

    add_h3("Aksi Layar & Perintah yang Dijalankan M. Naufal Widiatmoko:")
    add_lead_paragraph(
        "1. Di terminal SSH VM 2, tampilkan konfigurasi upstream Nginx:\n"
        "   Perintah: cat /etc/nginx/sites-available/default"
    )

    add_code_block(
        "Konfigurasi Upstream Round-Robin Nginx di VM 2",
        "cat /etc/nginx/sites-available/default | grep -A 14 'upstream backend_servers'",
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

    add_lead_paragraph(
        "2. Di terminal PowerShell Host Windows, jalankan pengujian pembagian beban 6 kali berturut-turut ke IP VM 2:"
    )

    add_code_block(
        "Uji Distribusi Beban Round-Robin dari Host PowerShell",
        "for ($i=1; $i -le 6; $i++) { (Invoke-RestMethod -Uri 'http://192.168.56.102/api/health').served_by }",
        "backend-node-1\n"
        "backend-node-2\n"
        "backend-node-1\n"
        "backend-node-2\n"
        "backend-node-1\n"
        "backend-node-2"
    )

    add_image_with_caption(
        "screenshots/03_VM2_Backend_Cluster_LoadBalancer/04_vm2_nginx_loadbalancer_upstream_conf.png",
        "Blok Konfigurasi Upstream dan Reverse Proxy Nginx Load Balancer di VM 2"
    )

    add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/02_uji_load_balancing_round_robin_curl.png",
        "Bukti Distribusi Beban Round-Robin 50:50 Bergantian Sempurna Antar Kontainer"
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # TAHAP 5: WEB DEMO, CRUD & FAILOVER TEST (MOH. YOGA DWI PRASETYO)
    # -------------------------------------------------------------------------
    add_h2("TAHAP 5: Demonstrasi Web SPA, Uji CRUD End-to-End, dan Uji Failover Chaos Test (Durasi: 4 Menit)")
    add_lead_paragraph(
        "Penanggung Jawab: Moh. Yoga Dwi Prasetyo (NIM: 240441100133)\n"
        "Peran: QA, Stress Testing & Documentation Lead"
    )

    add_dialogue_box(
        "Moh. Yoga Dwi Prasetyo",
        "QA & Testing Lead",
        "Terima kasih Mas Naufal Widiatmoko. Sekarang kita masuk ke pengujian fungsional dan uji ketahanan sistem (Chaos Test). "
        "Pertama, saya membuka browser di laptop host ke http://192.168.56.101. Halaman ini disajikan oleh Nginx di VM 1 "
        "dari build statis Single Page Application React 18. Antarmuka memiliki fitur filter instan, pencarian, pelaporan, "
        "dan integrasi WhatsApp. Sekarang saya akan melakukan uji aliran data penuh (CRUD End-to-End), lalu kita lakukan "
        "pengujian paling krusial, yaitu Failover Test dengan mematikan paksa salah satu kontainer backend."
    )

    add_h3("Aksi Layar 5A: Demonstrasi Web SPA & Uji Aliran Data (CRUD End-to-End)")
    add_lead_paragraph(
        "1. Buka browser host ke alamat: http://192.168.56.101\n"
        "2. Tunjukkan katalog barang, filter tab 'Barang Hilang', 'Barang Ditemukan', dan fitur search.\n"
        "3. Klik tombol '+ Lapor Barang Baru'.\n"
        "4. Masukkan data uji nyata:\n"
        "   - Judul: 'KTM Sistem Informasi an. Yoga Dwi'\n"
        "   - Kategori: Dokumen / KTM\n"
        "   - Tipe Laporan: Hilang\n"
        "   - Lokasi: Gedung Lab CBT FT UTM\n"
        "   - Kontak WA: 08123456789\n"
        "5. Klik 'Simpan Laporan' -> Data langsung tampil di kartu antarmuka tanpa refresh (SPA).\n"
        "6. Beralih ke terminal VM 3, jalankan query SQL untuk membuktikan data tersimpan permanen di MySQL:"
    )

    add_image_with_caption(
        "screenshots/02_VM1_Frontend_SPA/04_browser_portal_lost_and_found_home.png",
        "Antarmuka Single Page Application (SPA) Portal Campus Lost & Found pada Browser Host"
    )

    add_image_with_caption(
        "screenshots/02_VM1_Frontend_SPA/05_browser_form_lapor_barang_baru.png",
        "Formulir Pelaporan Barang Baru yang Terhubung Secara End-to-End ke Backend & Database"
    )

    add_code_block(
        "Verifikasi di MySQL VM 3 Bahwa Data Baru Benar-Benar Tersimpan",
        "docker exec -it mysql-database mysql -u root -prahasia123 lost_found_db -e \"SELECT id, title, contact_name, location FROM items ORDER BY id DESC LIMIT 1;\"",
        "+----+--------------------------------------+----------------+------------------------+\n"
        "| id | title                                | reporter_name  | location               |\n"
        "+----+--------------------------------------+----------------+------------------------+\n"
        "|  7 | KTM Sistem Informasi an. Yoga Dwi    | Yoga Dwi       | Gedung Lab CBT FT UTM  |\n"
        "+----+--------------------------------------+----------------+------------------------+"
    )

    add_h3("Aksi Layar 5B: Uji Ketahanan Sistem (Failover Chaos Test — Poin Nilai A ⭐)")
    add_lead_paragraph(
        "Dosen penguji ingin melihat apakah website mati jika ada server backend yang crash:"
    )

    add_lead_paragraph(
        "1. Di terminal SSH VM 2, matikan secara paksa kontainer backend-1:\n"
        "   Perintah: docker stop backend-node-1\n"
        "2. Di terminal PowerShell Host, jalankan loop request kembali:"
    )

    add_code_block(
        "Hasil Pengujian Failover Saat backend-node-1 Mati",
        "for ($i=1; $i -le 4; $i++) { (Invoke-RestMethod -Uri 'http://192.168.56.102/api/health').served_by }",
        "backend-node-2\n"
        "backend-node-2\n"
        "backend-node-2\n"
        "backend-node-2\n"
        "# KESIMPULAN: 100% Request berhasil dialihkan ke backend-node-2 tanpa error 502/downtime!"
    )

    add_lead_paragraph(
        "3. Buka browser host (http://192.168.56.101), lakukan refresh dan input data baru. "
        "Buktikan website 100% NORMAL dan tidak menampilkan layar error!\n"
        "4. Di terminal SSH VM 2, pulihkan kembali kontainer backend-1:\n"
        "   Perintah: docker start backend-node-1\n"
        "5. Jalankan loop request lagi: Nginx otomatis mendeteksi node yang telah sembuh dan "
        "membagi beban kembali secara Round-Robin 50:50."
    )

    add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/03_uji_failover_simulasi_node1_down.png",
        "Bukti Zero-Downtime Failover: Traffic Otomatis Dialihkan 100% ke backend-node-2"
    )

    add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/04_uji_failover_recovery_node1.png",
        "Bukti Pemulihan Otomatis (Auto-Recovery): Beban Kembali Seimbang Setelah Node 1 Dinyalakan"
    )

    # -------------------------------------------------------------------------
    # TAHAP 6: PENUTUP & RANGKUMAN (ATTALA)
    # -------------------------------------------------------------------------
    add_h2("TAHAP 6: Kesimpulan Ketercapaian Rubrik & Penutup (Durasi: 1 Menit)")
    add_lead_paragraph(
        "Penanggung Jawab: Attala Alif Ramadhani Tri Hida (NIM: 230441100144)\n"
        "Peran: Ketua Kelompok"
    )

    add_dialogue_box(
        "Attala Alif Ramadhani Tri Hida",
        "Ketua Kelompok",
        "Demikian demonstrasi sistem 'Campus Lost & Found' dari kelompok kami. Dari pengujian tadi, kami telah membuktikan "
        "bahwa arsitektur Multi-VM Type-2 VirtualBox kami telah memenuhi 100% rubrik penilaian: pemisahan 3 VM, "
        "SPA frontend, cluster 2 instance backend, load balancer Round-Robin, ketahanan failover tanpa downtime, "
        "dan persistent database container. Terima kasih atas perhatian Pak Firman, waktu dan tempat kami persilakan "
        "untuk sesi tanya jawab."
    )

    doc.add_page_break()

    # =========================================================================
    # BAB 4: KUNCI JAWABAN PERTANYAAN DOSEN (Q&A DEFENSE GUIDE)
    # =========================================================================
    add_h1("BAB 4: KUNCI JAWABAN PERTANYAAN KRITIS DOSEN (Q&A DEFENSE GUIDE)")

    add_lead_paragraph(
        "Bab ini berisi panduan jawaban teknis berbobot untuk mengantisipasi pertanyaan mendalam yang sering diajukan "
        "oleh Dosen Pengampu (Pak Firman) saat sesi tanya jawab."
    )

    qa_list = [
        (
            "Q1: Mengapa menggunakan Adapter 'Host-Only' VirtualBox, bukan 'Bridged' atau 'NAT'?",
            "Penjawab yang Tepat: Attala Alif Ramadhani Tri Hida (Infra Lead)",
            "Jawaban Teknis:\n"
            "1. Isolasi dan Keamanan: Host-Only Network menciptakan subnet privat virtual (192.168.56.0/24) yang hanya bisa diakses "
            "oleh laptop host dan ketiga VM. Jaringan ini terisolasi dari gangguan luar seperti Wi-Fi publik kampus.\n"
            "2. Kepastian Alamat IP: Pada mode Bridged, IP VM didapatkan dari router Wi-Fi yang berubah-ubah saat berpindah lokasi. "
            "Dengan Host-Only dan Netplan statis, IP VM dijamin selalu konsisten (.101, .102, .103) sehingga konfigurasi Load Balancer "
            "dan koneksi database tidak pernah putus."
        ),
        (
            "Q2: Bagaimana Docker Persistent Volume menjamin data tidak hilang saat kontainer MySQL dimatikan?",
            "Penjawab yang Tepat: Tanji (Database Specialist)",
            "Jawaban Teknis:\n"
            "Secara default, kontainer Docker bersifat 'ephemeral' (data di dalam layer kontainer hilang saat dihapus). "
            "Untuk mengatasinya, kami menggunakan Docker Named Volume 'lost_found_mysql_data' yang memetakan folder data database "
            "di dalam kontainer (/var/lib/mysql) langsung ke direktori penyimpanan fisik disk host VM 3 (/var/lib/docker/volumes/...). "
            "Dengan demikian, siklus hidup data (data lifecycle) terpisah dari siklus hidup kontainer (container lifecycle). "
            "Meskipun kontainer di-stop, di-restart, atau diganti versinya, blok data InnoDB tetap utuh di disk VM 3."
        ),
        (
            "Q3: Bagaimana Nginx Load Balancer mendeteksi backend yang mati dan melakukan failover?",
            "Penjawab yang Tepat: Muhammad Naufal Widiatmoko (Load Balancer Engineer)",
            "Jawaban Teknis:\n"
            "Kami mengonfigurasi dua parameter penting pada blok upstream Nginx:\n"
            "- 'max_fails=2' dan 'fail_timeout=5s': Jika sebuah instance backend gagal merespons request sebanyak 2 kali berturut-turut, "
            "Nginx akan menandai node tersebut sebagai 'inaktif' selama 5 detik.\n"
            "- 'proxy_next_upstream error timeout http_500 http_502 http_503': Ketika Nginx meneruskan request ke backend-node-1 dan "
            "menerima error koneksi, Nginx tidak meneruskan error tersebut ke browser klien, melainkan langsung mengarahkan request yang sama "
            "ke node berikutnya (backend-node-2) dalam hitungan milidetik. Inilah yang mewujudkan 'Zero-Downtime Failover'."
        ),
        (
            "Q4: Mengapa aplikasi backend harus dijalankan minimal 2 instance di VM 2?",
            "Penjawab yang Tepat: Naufal Husain (Backend Specialist)",
            "Jawaban Teknis:\n"
            "Dalam prinsip arsitektur Cloud Computing, menjalankan hanya 1 instance aplikasi menciptakan 'Single Point of Failure' (SPoF). "
            "Jika proses server tersebut mengalami memory leak, crash, atau restart, seluruh layanan akan padam total. "
            "Dengan menjalankan 2 kontainer kembar (backend-node-1 dan backend-node-2), sistem memiliki 'Redundancy' dan 'High Availability'. "
            "Selain itu, throughput sistem meningkat karena beban komputasi CPU dibagi dua oleh Load Balancer."
        ),
        (
            "Q5: Kenapa Frontend di-build menjadi file statis (npm run build) dan disajikan lewat Nginx di VM 1, bukan menjalankan 'npm run dev'?",
            "Penjawab yang Tepat: Tanji / Yoga Dwi Prasetyo",
            "Jawaban Teknis:\n"
            "1. Standar Production: Perintah 'npm run dev' menjalankan Node development server dengan modul Hot Module Replacement (HMR) "
            "yang memakan resource RAM besar dan rentan crash. "
            "2. Kinerja Tinggi: Dengan 'npm run build', kode React di-kompilasi dan di-minifikasi menjadi bundle HTML, CSS, dan JS murni. "
            "Nginx di VM 1 bertindak sebagai web server statis berbasis event-driven (epoll) yang mampu melayani ribuan request per detik "
            "dengan konsumsi RAM sangat rendah (< 30 MB)."
        ),
        (
            "Q6: Bagaimana mekanisme Cross-Origin Resource Sharing (CORS) diselesaikan pada sistem ini?",
            "Penjawab yang Tepat: Naufal Husain / Muhammad Naufal Widiatmoko",
            "Jawaban Teknis:\n"
            "Frontend berjalan pada origin 'http://192.168.56.101', sedangkan API backend berada pada 'http://192.168.56.102'. "
            "Browser akan menerapkan aturan Same-Origin Policy. Kami menyelesaikan masalah ini dengan mengaktifkan middleware 'cors()' "
            "pada layer Express.js backend dan memastikan tidak ada duplikasi header 'Access-Control-Allow-Origin' di Nginx Load Balancer, "
            "sehingga browser mengizinkan pertukaran data JSON secara aman tanpa diblokir."
        ),
        (
            "Q7: Apa perbedaan Type-1 Hypervisor dan Type-2 Hypervisor? Mengapa proyek ini memakai Type-2?",
            "Penjawab yang Tepat: Attala Alif Ramadhani Tri Hida (Ketua)",
            "Jawaban Teknis:\n"
            "- Type-1 (Bare-Metal): Hypervisor berjalan langsung di atas hardware fisik tanpa OS perantara (contoh: VMware ESXi, Proxmox VE). "
            "Biasanya diterapkan di data center server dedicated.\n"
            "- Type-2 (Hosted): Hypervisor berjalan sebagai aplikasi software di atas Host OS yang sudah ada (contoh: Oracle VM VirtualBox di atas Windows 11).\n"
            "Alasan Penggunaan: Karena batasan perangkat keras pengujian menggunakan laptop pribadi mahasiswa, Type-2 Hypervisor adalah "
            "pilihan paling ideal dan tepat guna untuk mensimulasikan lingkungan cloud terdistribusi multi-server tanpa menghapus sistem operasi laptop."
        ),
        (
            "Q8: Bagaimana keamanan akses database di VM 3 dijaga?",
            "Penjawab yang Tepat: Tanji / Attala Alif",
            "Jawaban Teknis:\n"
            "1. Database MySQL di VM 3 (Port 3306) hanya diizinkan untuk diakses oleh subnet private internal. "
            "2. Akses MySQL dikonfigurasi pada subnet privat Host-Only 192.168.56.0/24 khusus melayani koneksi dari VM 2, "
            "tanpa mengekspos port 3306 ke jaringan publik maupun akses langsung dari layer Frontend.\n"
            "3. Frontend di VM 1 sama sekali tidak memiliki akses langsung ke port 3306; seluruh komunikasi data wajib melalui perantara "
            "REST API di VM 2 demi kepatuhan prinsip arsitektur 3-Tier yang aman."
        )
    ]

    for q_title, q_resp, q_body in qa_list:
        add_h2(q_title)
        add_lead_paragraph(f"👤 {q_resp}")
        add_callout("JAWABAN TEKNIS LENGKAP", q_body, callout_type="success")

    doc.add_page_break()

    # =========================================================================
    # BAB 5: PROSEDUR MEMATIKAN SISTEM SECARA BERSIH (CLEAN SHUTDOWN GUIDE)
    # =========================================================================
    add_h1("BAB 5: PROSEDUR MEMATIKAN SISTEM SECARA BERSIH (CLEAN SHUTDOWN)")

    add_lead_paragraph(
        "Setelah sesi demonstrasi dan ujian selesai, sistem Virtual Machine HARUS DIMATIKAN SECARA BERURUTAN "
        "(Clean Graceful Shutdown). Mematikan VM secara mendadak atau mematikan laptop langsung dapat menyebabkan "
        "korupsi tabel InnoDB pada database MySQL."
    )

    add_h2("5.1 Urutan Mematikan Virtual Machine (Graceful Shutdown Order)")
    add_lead_paragraph(
        "Urutan mematikan adalah KEBALIKAN dari urutan menyalakan sistem:"
    )

    down_headers = ["Urutan", "Virtual Machine", "Perintah Shutdown di Terminal SSH", "Penjelasan Keamanan"]
    down_data = [
        ["1 (Pertama)", "VM1-Frontend (192.168.56.101)", "sudo poweroff", "Matikan web server frontend terlebih dahulu agar tidak ada lagi user baru yang mengirim request."],
        ["2 (Kedua)", "VM2-Backend (192.168.56.102)", "sudo poweroff", "Matikan Load Balancer dan kontainer backend setelah seluruh request yang sedang berjalan selesai diproses."],
        ["3 (Ketiga / Terakhir)", "VM3-Database (192.168.56.103)", "sudo poweroff", "Matikan database terakhir setelah tidak ada lagi query transaksi dari backend. Engine MySQL melakukan buffer flush ke disk secara aman."],
    ]
    add_styled_table(down_headers, down_data, [1.0, 1.8, 1.7, 2.0])

    add_h2("5.2 Alternatif Mematikan Bersih dari Host Windows PowerShell")
    add_lead_paragraph(
        "Jika Anda ingin mematikan ketiga VM sekaligus tanpa membuka jendela terminal SSH satu per satu, "
        "jalankan skrip PowerShell berikut di laptop host:"
    )

    add_code_block(
        "Skrip Satu Baris Mematikan Seluruh VM Secara Graceful dari Host",
        '"VM1-Frontend", "VM2-Backend", "VM3-Database" | ForEach-Object { & "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe" controlvm $_ acpipowerbutton }',
        "# Penjelasan: Sinyal ACPI Power Button akan memicu shutdown resmi pada kernel Ubuntu Server,\n"
        "# menutup seluruh servis secara anggun tanpa risiko kerusakan data."
    )

    doc.add_page_break()

    # =========================================================================
    # LAMPIRAN: CHEAT-SHEET PERINTAH CEPAT LIVE DEMO
    # =========================================================================
    add_h1("LAMPIRAN: LEMBAR CONTEKAN CEPAT PERINTAH TERMINAL (CHEAT-SHEET)")

    add_lead_paragraph(
        "Lembar ini dapat dicetak atau ditampilkan pada smartphone/layar kedua saat presentasi "
        "sebagai panduan darurat perintah command line:"
    )

    cheat_headers = ["Tahap Demo", "Mesin / Terminal", "Perintah Command Line", "Tujuan Verifikasi"]
    cheat_data = [
        ["Tahap 1", "PowerShell Host", "Test-Connection 192.168.56.101, 192.168.56.102, 192.168.56.103 -Count 1", "Uji konektivitas ping 3 VM sekaligus"],
        ["Tahap 2", "SSH VM3 (.103)", "docker ps", "Status kontainer mysql-database Up 3306"],
        ["Tahap 2", "SSH VM3 (.103)", "docker volume ls", "Membuktikan volume persistent lost_found_mysql_data"],
        ["Tahap 2", "SSH VM3 (.103)", "docker exec -it mysql-database mysql -u root -prahasia123 lost_found_db -e \"SELECT * FROM items;\"", "Membuktikan isi tabel database tersimpan"],
        ["Tahap 3", "SSH VM2 (.102)", "cat ~/backend/docker-compose.yml", "Menampilkan konfigurasi 2 instance backend"],
        ["Tahap 3", "SSH VM2 (.102)", "docker ps", "Status backend-node-1 (5001) & backend-node-2 (5002) Up"],
        ["Tahap 4", "SSH VM2 (.102)", "cat /etc/nginx/sites-available/default", "Menampilkan konfigurasi upstream Load Balancer"],
        ["Tahap 4", "PowerShell Host", "for ($i=1;$i -le 6;$i++) { (Invoke-RestMethod 'http://192.168.56.102/api/health').served_by }", "Uji distribusi beban Round-Robin 50:50"],
        ["Tahap 5", "Browser Host", "Buka http://192.168.56.101", "Demo UI SPA React, Filter, & Form Lapor Baru"],
        ["Tahap 5", "SSH VM2 (.102)", "docker stop backend-node-1", "Simulasi CHAOS TEST: Matikan paksa backend node 1"],
        ["Tahap 5", "PowerShell Host", "for ($i=1;$i -le 4;$i++) { (Invoke-RestMethod 'http://192.168.56.102/api/health').served_by }", "Membuktikan 100% request dialihkan ke node 2 (Failover)"],
        ["Tahap 5", "SSH VM2 (.102)", "docker start backend-node-1", "Memulihkan kembali backend node 1 (Auto-Recovery)"],
    ]
    add_styled_table(cheat_headers, cheat_data, [0.8, 1.2, 2.7, 1.8])

    return doc

if __name__ == "__main__":
    output_filename = "LAPORAN_PANDUAN_LIVE_DEMO_CLOUD_COMPUTING.docx"
    print(f"Generating Word document: {output_filename} ...")
    document = create_document()
    document.save(output_filename)
    file_size_kb = os.path.getsize(output_filename) / 1024
    print(f"Successfully generated: {output_filename} ({file_size_kb:.2f} KB)")
