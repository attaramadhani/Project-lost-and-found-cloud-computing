# -*- coding: utf-8 -*-
"""
Generator Panduan Teknis & SOP Lengkap Tahap 3: Backend Cluster Multi-Instance Docker
Untuk: Naufal Husain (240441100038) & Tim Cloud Computing UTM
Dosen Pengampu: Firmansyah Adiputra, S.T., M.Sc.
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

def build_tahap3_guide():
    doc = Document()

    # Configure Margins
    for section in doc.sections:
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
        hrun = hp.add_run("Panduan SOP Tahap 3: Backend Multi-Instance Docker — Cloud Computing UTM")
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Penanggung Jawab: Naufal Husain (240441100038) | Dosen: Firmansyah Adiputra, S.T., M.Sc.")
        frun.font.name = 'Calibri'
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Styling Constants
    COLOR_PRIMARY = RGBColor(30, 58, 138)    # #1E3A8A - UTM Dark Navy
    COLOR_SECONDARY = RGBColor(37, 99, 235)  # #2563EB - Royal Blue
    COLOR_DARK = RGBColor(15, 23, 42)        # #0F172A - Slate 900
    COLOR_MUTED = RGBColor(71, 85, 105)      # #475569 - Slate 600
    COLOR_GREEN = RGBColor(22, 101, 52)      # #166534 - Forest Green
    COLOR_AMBER = RGBColor(180, 83, 9)       # #B45309 - Amber Dark

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_DARK
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

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

    def add_code_block(title, command_str, explanation=None, expected_output=None):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)

        cell = tbl.cell(0, 0)
        set_cell_margins(cell, top=110, bottom=110, left=140, right=120)
        set_cell_background(cell, "0F172A") # Dark slate
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
        r_cmd.font.color.rgb = RGBColor(56, 189, 248) # Cyan

        if expected_output:
            r_out_lbl = p.add_run("# Output Terminal yang Diharapkan:\n")
            r_out_lbl.font.name = 'Consolas'
            r_out_lbl.font.size = Pt(8)
            r_out_lbl.font.color.rgb = RGBColor(148, 163, 184)

            r_out = p.add_run(f"{expected_output}\n")
            r_out.font.name = 'Consolas'
            r_out.font.size = Pt(8.5)
            r_out.font.color.rgb = RGBColor(241, 245, 249)

        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_styled_table(headers, data, col_widths=None):
        tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
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
                run.font.color.rgb = COLOR_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image_with_caption(img_path, caption, width=Inches(5.6)):
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
    # COVER PAGE
    # =========================================================================
    p_cov_top = doc.add_paragraph()
    p_cov_top.paragraph_format.space_before = Pt(16)
    p_cov_top.paragraph_format.space_after = Pt(8)
    p_cov_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_univ = p_cov_top.add_run("UNIVERSITAS TRUNOJOYO MADURA\nFAKULTAS TEKNIK — PROGRAM STUDI S1 SISTEM INFORMASI\n")
    r_univ.bold = True
    r_univ.font.size = Pt(12)
    r_univ.font.color.rgb = COLOR_PRIMARY

    r_div = p_cov_top.add_run("━" * 45 + "\n")
    r_div.font.color.rgb = COLOR_SECONDARY

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("PANDUAN LENGKAP & STANDAR OPERASIONAL (SOP)\nTAHAP 3: PEMBUKTIAN BACKEND CLUSTER\nMINIMAL 2 INSTANCE CONTAINER DOCKER\n")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(
        "\"Buku Panduan Komprehensif Eksekusi Live Demo Dari Awal Persiapan Hingga Selesai, "
        "Pembedahan Fungsi Seluruh Perintah Terminal, Script Dialog Presenter, dan Kunci Jawaban Penguji\""
    )
    r_sub.italic = True
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = COLOR_MUTED

    p_dosen = doc.add_paragraph()
    p_dosen.paragraph_format.space_before = Pt(4)
    p_dosen.paragraph_format.space_after = Pt(8)
    p_dosen.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dosen = p_dosen.add_run("Dosen Pengampu:\n")
    r_dosen.font.size = Pt(10.5)
    r_dosen_name = p_dosen.add_run("Firmansyah Adiputra, S.T., M.Sc.\n")
    r_dosen_name.bold = True
    r_dosen_name.font.size = Pt(11.5)
    r_dosen_name.font.color.rgb = COLOR_PRIMARY

    # Profile Box on Cover
    profil_headers = ["Informasi Penanggung Jawab", "Detail Teknis"]
    profil_data = [
        ["Nama Mahasiswa", "Naufal Husain"],
        ["Nomor Induk Mahasiswa (NIM)", "240441100038"],
        ["Peran Tim (Role)", "Backend & Containerization Specialist"],
        ["Mesin / Target Server", "VM 2: Backend & Load Balancer (IP: 192.168.56.102)"],
        ["Tugas Pokok Tahap 3", "Pembuktian 2 Instance Container Docker (Port 5001 & 5002)"],
        ["Tugas Dukungan Tahap 5", "Simulasi Chaos Failover Test (docker stop / start backend-node-1)"],
    ]
    add_styled_table(profil_headers, profil_data, [2.5, 4.0])

    p_foot_cov = doc.add_paragraph()
    p_foot_cov.paragraph_format.space_before = Pt(12)
    p_foot_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot_cov.add_run("BANGKALAN — JAWA TIMUR\nTAHUN AKADEMIK 2024/2025")
    r_foot.bold = True
    r_foot.font.size = Pt(10)
    r_foot.font.color.rgb = COLOR_PRIMARY

    doc.add_page_break()

    # =========================================================================
    # BAB 1: LANDASAN TEORI & ARSITEKTUR BACKEND CLUSTER
    # =========================================================================
    add_h1("BAB 1: LANDASAN TEORI & ARSITEKTUR BACKEND CLUSTER")

    add_h2("1.1 Mengapa Dosen Mewajibkan 'Minimal 2 Instance Application Server'?")
    add_lead_paragraph(
        "Dalam mata kuliah Cloud Computing, salah satu prinsip paling fundamental adalah menghindari "
        "Single Point of Failure (SPoF). Jika sistem hanya mengandalkan 1 proses aplikasi tunggal (misal hanya menjalankan "
        "'node server.js'), maka ketika server mengalami kegagalan (crash akibat unhandled rejection, memory leak, atau maintenance), "
        "seluruh layanan kampus akan mati total. Dosen pengampu (Pak Firman) mewajibkan minimal 2 instance untuk menilai "
        "kemampuan mahasiswa dalam merancang sistem yang memiliki Redundancy dan High Availability (ketersediaan tinggi)."
    )

    add_h2("1.2 Konsep Containerization Menggunakan Docker")
    add_lead_paragraph(
        "Aplikasi backend Express.js dikemas menggunakan Docker berbasis image 'node:20-alpine'. "
        "Kelebihan pendekatan ini:"
    )
    add_lead_paragraph(
        "1. Isolasi Lingkungan: Setiap kontainer memiliki filesystem, library dependensi, network namespace, dan PID sendiri.\n"
        "2. Portabilitas Mutlak: Menghilangkan masalah 'works on my machine'. Kontainer berjalan persis sama di laptop host maupun di server VM2.\n"
        "3. Ukuran Ringan: Berbasis Alpine Linux dengan footprint memori sangat efisien (< 50 MB RAM per instance)."
    )

    add_h2("1.3 Pembedahan Port Mapping: Port Internal vs Port Eksternal")
    add_lead_paragraph(
        "Banyak mahasiswa keliru saat ditanya dosen mengenai pemetaan port. Berikut pembedahan logisnya:"
    )

    port_headers = ["Instance Kontainer", "Port Internal (Dalam Docker)", "Port Eksternal (Host VM2)", "Alasan Pemetaan"]
    port_data = [
        ["backend-node-1", "Port 5000", "Port 5001", "Di dalam kontainer, Express mendengarkan port default 5000. Di host VM2, soket diikat ke 5001 agar tidak tabrakan dengan instance lain."],
        ["backend-node-2", "Port 5000", "Port 5002", "Express di kontainer kedua juga mendengarkan port 5000 (karena namespace jaringan terisolasi). Di host VM2, soket diikat ke 5002."],
    ]
    add_styled_table(port_headers, port_data, [1.5, 1.4, 1.4, 2.2])

    add_h2("1.4 Injeksi Metadata: Transparansi Pengenalan Instance")
    add_lead_paragraph(
        "Agar kita dan dosen bisa membuktikan secara objektif kontainer mana yang merespons permintaan, "
        "pada berkas server.js disuntikkan middleware kustom yang mengambil nilai dari Environment Variable APP_INSTANCE:"
    )

    add_code_block(
        "Cuplikan Middleware Metadata pada backend/server.js",
        "const INSTANCE_NAME = process.env.APP_INSTANCE || `backend-${os.hostname()}`;\n"
        "app.use((req, res, next) => {\n"
        "  res.setHeader('X-Served-By', INSTANCE_NAME);\n"
        "  next();\n"
        "});",
        "Setiap response HTTP otomatis menyertakan identitas kontainer baik di HTTP Header maupun JSON body."
    )

    add_image_with_caption(
        "screenshots/01_Arsitektur_dan_Ketentuan/02_diagram_arsitektur_aplikasi_3tier.png",
        "Posisi Backend Cluster Multi-Instance pada Arsitektur 3-Tier Terdistribusi"
    )

    doc.add_page_break()

    # =========================================================================
    # BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (FASE PRE-FLIGHT)
    # =========================================================================
    add_h1("BAB 2: PANDUAN PERSIAPAN SEBELUM PRESENTASI (FASE PRE-FLIGHT)")

    add_lead_paragraph(
        "Bab ini memandu Naufal Husain untuk memastikan seluruh servis backend di VM 2 dalam kondisi prima "
        "SEBELUM kelompok dipanggil ke depan kelas."
    )

    add_h2("2.1 Urutan Menjalankan VM & Ketergantungan Servis Backend")
    add_lead_paragraph(
        "Ingat! Backend di VM 2 membutuhkan koneksi ke Database MySQL di VM 3. "
        "Oleh karena itu, pastikan urutan berikut dipatuhi:"
    )
    add_lead_paragraph(
        "1. Pastikan VM3 (Database: 192.168.56.103) sudah UP terlebih dahulu.\n"
        "2. Nyalakan VM2 (Backend: 192.168.56.102).\n"
        "3. Tunggu 15-20 detik agar Docker daemon di VM2 selesai melakukan auto-start kontainer."
    )

    add_h2("2.2 Cara Menjalankan Pertama Kali / Rebuild Kontainer (Jika Belum Berjalan)")
    add_lead_paragraph(
        "Jika kontainer belum pernah dijalankan atau baru saja ada perubahan kode, lakukan langkah inisialisasi berikut di terminal VM2:"
    )

    add_code_block(
        "Inisialisasi & Up Kontainer Backend di VM 2",
        "cd ~/backend\ndocker compose up -d --build",
        "Membangun image dari Dockerfile dan menjalankan kedua kontainer di background mode (-d).",
        "[+] Building 4.2s (10/10) FINISHED\n"
        "[+] Running 2/2\n"
        " ✔ Container backend-node-1  Started\n"
        " ✔ Container backend-node-2  Started"
    )

    add_h2("2.3 Checklist Kesiapan Sebelum Giliran Presentasi")
    check_headers = ["No", "Parameter Kesiapan", "Perintah Cepat di VM2", "Kondisi Lolos (PASS)"]
    check_data = [
        ["1", "Docker Daemon Aktif", "sudo systemctl is-active docker", "Output: active"],
        ["2", "Status 2 Kontainer", "docker ps", "Menampilkan backend-node-1 dan backend-node-2 status Up"],
        ["3", "Health Node 1 (5001)", "curl -s http://localhost:5001/api/health", "JSON: status 'healthy', served_by 'backend-node-1'"],
        ["4", "Health Node 2 (5002)", "curl -s http://localhost:5002/api/health", "JSON: status 'healthy', served_by 'backend-node-2'"],
        ["5", "Koneksi Database MySQL", "docker logs --tail 5 backend-node-1", "Muncul log: Connected to MySQL Database at 192.168.56.103"],
    ]
    add_styled_table(check_headers, check_data, [0.4, 1.8, 2.3, 2.0])

    doc.add_page_break()

    # =========================================================================
    # BAB 3: ALUR KERJA KESELURUHAN & TITIK MASUK (ESTAFET TIM)
    # =========================================================================
    add_h1("BAB 3: ALUR KERJA KESELURUHAN & TITIK MASUK (ESTAFET TIM)")

    add_lead_paragraph(
        "Agar presentasi kelompok mengalir secara mulus tanpa canggung, pahami alur estafet peran Anda dari awal hingga akhir:"
    )

    alur_headers = ["Tahap Demo", "Presenter", "Fokus Bahasan", "Peran & Keterkaitan Naufal Husain"]
    alur_data = [
        ["Tahap 1 (2 Menit)", "Attala Alif", "Pembukaan & Uji Ping Multi-VM", "Menyiapkan terminal tab SSH ke VM2 di layar laptop."],
        ["Tahap 2 (3 Menit)", "Tanji", "Database & Persistent Volume VM3", "Memperhatikan kesiapan DB di .103 yang menjadi dependensi backend."],
        ["Tahap 3 (3 Menit)", "Naufal Husain (ANDA)", "Pembuktian 2 Instance Container VM2", "EKSEKUSI UTAMA: Menerima estafet, mendemokan compose, docker ps, dan curl internal."],
        ["Tahap 4 (3 Menit)", "M. Naufal Widiatmoko", "Load Balancer Round-Robin Nginx", "Menjelaskan bahwa 2 instance yang Anda buat diikat oleh upstream LB rekan Anda."],
        ["Tahap 5 (4 Menit)", "Moh. Yoga Dwi", "Uji Web CRUD & Failover Chaos Test", "EKSEKUSI DUET: Naufal mengeksekusi 'docker stop backend-node-1' untuk uji failover!"],
        ["Tahap 6 (1 Menit)", "Attala Alif", "Kesimpulan Rubrik & Q&A Dosen", "Menjawab pertanyaan dosen terkait Docker, port mapping, dan backend logic."],
    ]
    add_styled_table(alur_headers, alur_data, [1.1, 1.3, 1.9, 2.2])

    add_h2("3.1 Titik Serah Terima Estafet (Handover Transition)")
    add_lead_paragraph(
        "Kalimat transisi yang akan diucapkan oleh Mas Tanji sebelum Anda mulai bicara:"
    )
    add_callout(
        "KALIMAT OPERAN DARI MAS TANJI (TAHAP 2)",
        "\"...Demikian pembuktian database MySQL 8 dengan persistent storage di VM 3. Selanjutnya, untuk pembuktian minimal "
        "2 instance backend application server di VM 2, saya serahkan kepada rekan saya Naufal Husain. Silakan Mas Naufal.\"",
        callout_type="info"
    )

    doc.add_page_break()

    # =========================================================================
    # BAB 4: PELAKSANAAN DEMO TAHAP 3 LANGKAH DEMI LANGKAH (EKSEKUSI LIVE)
    # =========================================================================
    add_h1("BAB 4: PELAKSANAAN DEMO TAHAP 3 LANGKAH DEMI LANGKAH (EKSEKUSI LIVE)")

    add_lead_paragraph(
        "Saat giliran Anda tiba, tatap Dosen Pengampu dengan tenang, ucapkan script bicara, "
        "lalu eksekusi perintah secara berurutan sesuai panduan berikut:"
    )

    add_dialogue_box(
        "Naufal Husain",
        "Backend & Containerization Specialist",
        "Terima kasih Mas Tanji. Selamat pagi/siang Pak Firman. Pada VM 2 dengan IP 192.168.56.102, tugas utama saya adalah "
        "mengimplementasikan ketentuan 'minimal 2 instance application server'. Untuk menghindari Single Point of Failure, "
        "aplikasi backend Express.js telah kami kemas dalam Dockerfile berbasis Alpine Linux yang ringan, lalu diorkestrasi "
        "menggunakan Docker Compose menjadi dua kontainer independen yang berjalan bersamaan: backend-node-1 pada port 5001 "
        "dan backend-node-2 pada port 5002. Setiap kontainer menyuntikkan environment variable APP_INSTANCE sehingga setiap request "
        "dapat mengidentifikasi secara transparan kontainer mana yang melayani. Mari kita buktikan konfigurasinya langsung di terminal VM 2."
    )

    add_h2("Langkah 1: Remote Login SSH ke VM 2")
    add_code_block(
        "Koneksi SSH ke Mesin VM 2",
        "ssh atta@192.168.56.102",
        "Membuka sesi terminal jarak jauh terenkripsi ke Ubuntu Server VM 2.",
        "Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-generic x86_64)\n"
        "atta@vm2-backend:~$ "
    )

    add_h2("Langkah 2: Menuju Direktori Kerja Backend")
    add_code_block(
        "Pindah Direktori ke ~/backend",
        "cd ~/backend",
        "Masuk ke direktori repositori tempat berkas server.js, Dockerfile, dan docker-compose.yml berada.",
        "atta@vm2-backend:~/backend$ "
    )

    add_h2("Langkah 3: Membedah Konfigurasi Orkestrasi Docker Compose")
    add_lead_paragraph(
        "Tampilkan isi docker-compose.yml ke layar proyektor untuk membuktikan deklarasi 2 instance:"
    )
    add_code_block(
        "Menampilkan Berkas docker-compose.yml",
        "cat docker-compose.yml",
        "Membuktikan secara deklaratif adanya 2 service backend (backend-1 & backend-2) dengan port 5001 dan 5002.",
        "services:\n"
        "  backend-1:\n"
        "    build: .\n"
        "    container_name: backend-node-1\n"
        "    restart: always\n"
        "    ports: [\"5001:5000\"]\n"
        "    environment:\n"
        "      - APP_INSTANCE=backend-node-1\n"
        "      - DB_HOST=192.168.56.103\n"
        "  backend-2:\n"
        "    build: .\n"
        "    container_name: backend-node-2\n"
        "    restart: always\n"
        "    ports: [\"5002:5000\"]\n"
        "    environment:\n"
        "      - APP_INSTANCE=backend-node-2\n"
        "      - DB_HOST=192.168.56.103"
    )

    add_image_with_caption(
        "screenshots/03_VM2_Backend_Cluster_LoadBalancer/02_vm2_docker_compose_config.png",
        "Bukti Konfigurasi Deklaratif Minimal 2 Instance Backend pada docker-compose.yml"
    )

    add_h2("Langkah 4: Membuktikan Status Kedua Kontainer Berjalan Aktif")
    add_code_block(
        "Cek Status Kontainer Docker yang Sedang Berjalan",
        "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'",
        "Menampilkan tabel kontainer aktif tanpa kolom berantakan, menonjolkan nama kontainer, status Up, dan port.",
        "NAMES           STATUS         PORTS\n"
        "backend-node-1  Up 45 minutes  0.0.0.0:5001->5000/tcp\n"
        "backend-node-2  Up 45 minutes  0.0.0.0:5002->5000/tcp"
    )

    add_image_with_caption(
        "screenshots/03_VM2_Backend_Cluster_LoadBalancer/03_vm2_docker_ps_2_instances_running.png",
        "Dua Instance Backend Berjalan Bersamaan di Port 5001 dan 5002 pada VM 2"
    )

    add_h2("Langkah 5: Uji Health Check Langsung ke Masing-Masing Kontainer")
    add_lead_paragraph(
        "Buktikan bahwa kedua port tersebut benar-benar hidup dan menghasilkan identitas served_by yang berbeda:"
    )

    add_code_block(
        "Uji Respons Mandiri Kontainer 1 (Port 5001)",
        "curl -s http://localhost:5001/api/health",
        "Mengirim HTTP GET langsung ke soket port 5001 melewati bypass Load Balancer.",
        '{"status":"healthy","timestamp":"2026-10-29T...","served_by":"backend-node-1","hostname":"...","database":"connected","memory_usage_mb":45}'
    )

    add_code_block(
        "Uji Respons Mandiri Kontainer 2 (Port 5002)",
        "curl -s http://localhost:5002/api/health",
        "Mengirim HTTP GET langsung ke soket port 5002 melewati bypass Load Balancer.",
        '{"status":"healthy","timestamp":"2026-10-29T...","served_by":"backend-node-2","hostname":"...","database":"connected","memory_usage_mb":44}'
    )

    add_h2("Langkah 6 (Nilai Plus): Buktikan Pool Koneksi Database VM3")
    add_code_block(
        "Periksa Log Koneksi Database di Kedua Kontainer",
        "docker logs --tail 3 backend-node-1 && docker logs --tail 3 backend-node-2",
        "Menunjukkan output log stdout aplikasi Express yang mengonfirmasi koneksi sukses ke MySQL VM3 (192.168.56.103:3306).",
        "[backend-node-1] Connected to MySQL Database at 192.168.56.103:3306\n"
        "[backend-node-2] Connected to MySQL Database at 192.168.56.103:3306"
    )

    add_h2("Langkah 7: Menutup Tahap 3 & Menyerahkan Estafet ke Tahap 4")
    add_dialogue_box(
        "Naufal Husain",
        "Backend Specialist",
        "Kedua instance backend di port 5001 dan port 5002 telah terbukti aktif, sehat, dan terhubung ke database. "
        "Selanjutnya, rekan saya Muhammad Naufal Widiatmoko akan mendemonstrasikan bagaimana Nginx Load Balancer "
        "di port 80 membagi beban secara merata ke kedua instance ini menggunakan algoritma Round-Robin. Silakan Mas Widiatmoko."
    )

    doc.add_page_break()

    # =========================================================================
    # BAB 5: PERAN & TINDAKAN LANJUTAN HINGGA DEMO SELESAI (PASCA-TAHAP 3)
    # =========================================================================
    add_h1("BAB 5: PERAN & TINDAKAN LANJUTAN HINGGA DEMO SELESAI (PASCA-TAHAP 3)")

    add_lead_paragraph(
        "Setelah Tahap 3 selesai, tugas Naufal Husain BELUM SELESAI. Anda memiliki peran krusial pada Tahap 4, Tahap 5, "
        "dan Tahap 6 sebagai berikut:"
    )

    add_h2("5.1 Dukungan Saat Tahap 4 (Load Balancer Round-Robin)")
    add_lead_paragraph(
        "Saat Mas M. Naufal Widiatmoko menjalankan loop curl 6 kali di PowerShell host, "
        "pastikan Anda tetap berada di sesi terminal SSH VM 2. Jika Mas Widiatmoko membutuhkan verifikasi log akses, "
        "Anda dapat siap mengetikkan: 'docker logs -f backend-node-1' di tab kedua untuk melihat request masuk secara bergantian."
    )

    add_h2("5.2 DUET KRUSIAL PADA TAHAP 5: SIMULASI CHAOS FAILOVER TEST (POIN NILAI A ⭐)")
    add_lead_paragraph(
        "Pada Tahap 5, Moh. Yoga Dwi Prasetyo akan mendemokan ke dosen bahwa sistem tahan banting saat ada server crash. "
        "ANDA LAH YANG MENJADI EKSEKUTOR 'PEMBUNUH' DAN 'PENYELAMAT' KONTAINER:"
    )

    add_callout(
        "TINDAKAN ANDA SAAT UJI FAILOVER TAHAP 5",
        "1. Saat Yoga memberi aba-aba: 'Sekarang Mas Naufal akan mematikan kontainer node 1 secara paksa...'\n"
        "   👉 Anda ketik di terminal VM 2: docker stop backend-node-1\n"
        "2. Tunggu 2 detik hingga kontainer berhenti. Yoga akan menunjukkan browser host tetap jalan dan loop curl dialihkan 100% ke node 2.\n"
        "3. Saat Yoga memberi aba-aba: 'Sekarang Mas Naufal akan menyalakan kembali kontainer node 1...'\n"
        "   👉 Anda ketik di terminal VM 2: docker start backend-node-1\n"
        "4. Nginx Load Balancer langsung mendeteksi node 1 pulih dan kembali membagi beban seimbang 50:50!",
        callout_type="warning"
    )

    add_code_block(
        "Perintah Simulasi Crash & Recovery pada Tahap 5",
        "# 1. Matikan kontainer 1:\ndocker stop backend-node-1\n\n# 2. Nyalakan kembali kontainer 1:\ndocker start backend-node-1",
        "Perintah ini membuktikan mekanisme Zero-Downtime Failover dan Auto-Recovery di depan Dosen.",
        "backend-node-1 (Saat dimatikan)\nbackend-node-1 (Saat dinyalakan kembali)"
    )

    add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/03_uji_failover_simulasi_node1_down.png",
        "Bukti Uji Failover: Traffic Dialihkan Otomatis 100% ke backend-node-2 Saat backend-node-1 Dimatikan"
    )

    add_image_with_caption(
        "screenshots/05_Pengujian_LoadBalancing_dan_Failover/04_uji_failover_recovery_node1.png",
        "Bukti Auto-Recovery: Request Kembali Seimbang Begitu backend-node-1 Dinyalakan Kembali"
    )

    add_h2("5.3 Sikap & Kontribusi Saat Tahap 6 (Sesi Tanya Jawab Dosen)")
    add_lead_paragraph(
        "Saat Dosen Pengampu memberikan pertanyaan kritis mengenai backend, Node.js, atau Docker, "
        "Naufal Husain harus sigap dan percaya diri menjawab pertanyaan tersebut."
    )

    doc.add_page_break()

    # =========================================================================
    # BAB 6: PANDUAN TANYA JAWAB KRITIS (Q&A DEFENSE GUIDE) KHUSUS BACKEND
    # =========================================================================
    add_h1("BAB 6: PANDUAN TANYA JAWAB KRITIS (Q&A DEFENSE GUIDE) KHUSUS BACKEND")

    qa_backend = [
        (
            "Q1: Mengapa kedua kontainer backend bisa menggunakan port internal 5000 yang sama tanpa tabrakan (port conflict)?",
            "Jawaban Naufal Husain:\n"
            "\"Karena setiap kontainer Docker beroperasi di dalam Network Namespace yang sepenuhnya terisolasi. "
            "Bagi kontainer 1, ia memiliki interface loopback virtual sendiri yang mendengarkan di port 5000. "
            "Begitu pula dengan kontainer 2. Tabrakan port baru akan terjadi jika kita memetakan ke port Host OS yang sama. "
            "Di sini kita memetakan port Host yang berbeda, yaitu 5001 untuk kontainer 1 dan 5002 untuk kontainer 2, "
            "sehingga OS Ubuntu VM2 dapat membedakan traffic soket TCP keduanya secara sempurna.\""
        ),
        (
            "Q2: Apa bedanya menjalankan 2 instance lewat Docker Compose dibandingkan menjalankan PM2 cluster mode?",
            "Jawaban Naufal Husain:\n"
            "\"PM2 Cluster mode hanya membagi thread proses Node.js di atas satu OS host yang sama (process-level clustering). "
            "Sedangkan Docker Compose memberikan isolasi tingkat kontainer (container-level isolation). "
            "Dengan Docker, setiap instance memiliki alokasi memori (cgroups), dependensi OS, dan environment variable terisolasi. "
            "Jika satu kontainer mengalami memory leak parah atau segfault kernel modul, kontainer lainnya tetap aman dan tidak terpengaruh. "
            "Selain itu, pendekatan Docker adalah standar industri arsitektur cloud native yang kompatibel jika ke depan dimigrasi ke Kubernetes.\""
        ),
        (
            "Q3: Bagaimana jika salah satu kontainer backend mati mendadak saat ada user yang sedang mengirim data?",
            "Jawaban Naufal Husain:\n"
            "\"Di layer Nginx Load Balancer telah dikonfigurasikan parameter 'proxy_next_upstream error timeout http_500 http_502 http_503'. "
            "Artinya, jika Nginx meneruskan request ke kontainer 1 dan menerima timeout atau connection refused, "
            "Nginx tidak akan melempar error ke browser user, melainkan seketika memutar request tersebut ke kontainer 2 "
            "dalam hitungan milidetik. User di browser tidak merasakan gangguan apa pun (Zero Downtime).\""
        ),
        (
            "Q4: Mengapa memilih base image 'node:20-alpine' pada Dockerfile?",
            "Jawaban Naufal Husain:\n"
            "\"Alpine Linux dipilih karena memiliki ukuran image yang sangat kecil (sekitar 40 MB dibanding Ubuntu/Debian yang ratusan MB). "
            "Hal ini membuat proses download, build, dan startup kontainer menjadi sangat cepat (kurang dari 5 detik), "
            "serta mengurangi attack surface (celah keamanan) karena tidak memuat paket atau utilitas OS yang tidak diperlukan di production.\""
        ),
        (
            "Q5: Bagaimana jika traffic kampus naik 10 kali lipat saat masa wisuda/ospek? Bagaimana cara scaling backend ini?",
            "Jawaban Naufal Husain:\n"
            "\"Dengan arsitektur Docker Compose ini, kita memiliki opsi Horizontal Pod Autoscaling / Scaling. "
            "Kita cukup menambahkan 'backend-3' di port 5003 pada docker-compose.yml dan menambahkan satu baris 'server 127.0.0.1:5003' "
            "pada upstream Nginx, lalu reload service Nginx dalam 1 detik tanpa mematikan aplikasi yang sedang berjalan.\""
        )
    ]

    for q_t, q_a in qa_backend:
        add_h2(q_t)
        add_callout("KUNCI JAWABAN NAUFAL HUSAIN", q_a, callout_type="success")

    doc.add_page_break()

    # =========================================================================
    # BAB 7: PANDUAN PENANGANAN MASALAH CEPAT (TROUBLESHOOTING CHEAT SHEET)
    # =========================================================================
    add_h1("BAB 7: PANDUAN PENANGANAN MASALAH CEPAT (TROUBLESHOOTING CHEAT SHEET)")

    add_lead_paragraph(
        "Jika saat demo terjadi hal di luar dugaan, JANGAN PANIK! Gunakan panduan solusi instan berikut:"
    )

    add_h2("Kasus 1: Error 'port is already allocated' (Port 5001/5002 bentrok)")
    add_lead_paragraph("Gejala: Saat 'docker compose up', muncul pesan bind address already in use.")
    add_code_block(
        "Solusi Cepat Membunuh Proses Liar di Port 5001/5002",
        "sudo fuser -k 5001/tcp\nsudo fuser -k 5002/tcp\ndocker compose up -d",
        "Mematikan paksa proses orphan yang menyandera port dan menghidupkan kembali kontainer."
    )

    add_h2("Kasus 2: Kontainer Status 'Restarting' (Gagal Konek ke Database)")
    add_lead_paragraph("Gejala: 'docker ps' menunjukkan status Restarting (1) 5 seconds ago.")
    add_code_block(
        "Cek Log Error & Pastikan VM 3 MySQL UP",
        "docker logs --tail 20 backend-node-1\nping -c 2 192.168.56.103",
        "Biasanya terjadi karena VM3 belum hidup atau MySQL di VM3 belum selesai inisialisasi. Pastikan ping ke 192.168.56.103 sukses."
    )

    add_h2("Kasus 3: Perubahan Kode Belum Masuk ke Kontainer")
    add_lead_paragraph("Gejala: Kodingan server.js sudah diedit tetapi respons curl masih yang lama.")
    add_code_block(
        "Force Rebuild Kontainer Tanpa Cache",
        "cd ~/backend\ndocker compose down\ndocker compose build --no-cache\ndocker compose up -d",
        "Menghapus kontainer lama, membangun ulang image dari awal, dan mengangkat kontainer baru."
    )

    doc.add_page_break()

    # =========================================================================
    # BAB 8: PROSEDUR SHUTDOWN BERSIH KHUSUS VM2 (CLEAN EXIT)
    # =========================================================================
    add_h1("BAB 8: PROSEDUR SHUTDOWN BERSIH KHUSUS VM 2 (CLEAN EXIT)")

    add_lead_paragraph(
        "Setelah seluruh sesi live demo selesai dan Pak Firman menutup ujian, "
        "matikan layanan backend di VM 2 secara aman:"
    )

    add_code_block(
        "Prosedur Menghentikan Kontainer & Shutdown VM 2",
        "# 1. Hentikan kontainer dengan anggun:\ncd ~/backend && docker compose down\n\n# 2. Matikan mesin VM 2:\nsudo poweroff",
        "Menjamin seluruh proses Node.js dihentikan tanpa meninggalkan file lock atau status korup.",
        "[+] Running 2/2\n"
        " ✔ Container backend-node-1  Removed\n"
        " ✔ Container backend-node-2  Removed\n"
        "Connection to 192.168.56.102 closed by remote host."
    )

    add_callout(
        "RINGKASAN AKHIR UNTUK NAUFAL HUSAIN",
        "1. Kuasai script pembuka Tahap 3: Ucapkan dengan santai dan artikulatif.\n"
        "2. Hafalkan 3 perintah utama: 'cat docker-compose.yml', 'docker ps', dan 'curl ...:5001/api/health'.\n"
        "3. Standby di terminal VM 2 saat Tahap 5: Eksekusi 'docker stop backend-node-1' untuk memicu kekaguman dosen terhadap fitur Failover!\n"
        "4. Sukses untuk presentasi Anda dan kelompok!",
        callout_type="info"
    )

    return doc

if __name__ == "__main__":
    out_name = "PANDUAN_TEKNIS_TAHAP_3_BACKEND_CLUSTER_DOCKER.docx"
    print(f"Generating Word document: {out_name} ...")
    document = build_tahap3_guide()
    document.save(out_name)
    size_kb = os.path.getsize(out_name) / 1024
    print(f"Successfully created: {out_name} ({size_kb:.2f} KB)")
