"""
Module dựng file Word (.docx) chuẩn thể thức Nghị định 30/2020/NĐ-CP
Nguyên tắc: "Thể thức do mã, không do model"
Cung cấp API và CLI để tạo văn bản hành chính với bố cục, font chữ, lề và bảng chuẩn 100%.
"""

import os
import sys
from typing import List, Tuple, Optional

# Import các hằng số và quy chuẩn dùng chung
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from constants import (
    setup_windows_encoding,
    PAGE_WIDTH_MM,
    PAGE_HEIGHT_MM,
    MARGINS_DEFAULT_MM,
    FONT_FAMILY,
    get_standard_output_path,
    sanitize_dashes
)

setup_windows_encoding()

try:
    from docx import Document
    from docx.shared import Mm, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError:
    print("❌ Cần cài đặt python-docx: pip install python-docx")
    sys.exit(1)


def set_cell_margins(cell, top: int = 0, bottom: int = 0, left: int = 100, right: int = 100):
    """Thiết lập padding cho ô trong bảng để căn sát lề (đơn vị: dxa)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m_name, m_val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m_name}')
        node.set(qn('w:w'), str(m_val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def remove_table_borders(table):
    """Xóa toàn bộ đường viền của bảng (Borderless Table)"""
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        tblBorders.append(border)
    tblPr.append(tblBorders)


def add_page_number_to_header(section):
    """
    Thiết lập số trang văn bản chuẩn Nghị định 30:
    - Ở chính giữa lề trên (Header center)
    - Phông Times New Roman, cỡ 13–14pt
    - Không hiển thị ở trang đầu tiên (different_first_page_header_footer = True)
    """
    section.different_first_page_header_footer = True
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    # Chèn trường XML PAGE cho số trang
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFont = OxmlElement('w:rFonts')
    rFont.set(qn('w:ascii'), FONT_FAMILY)
    rFont.set(qn('w:hAnsi'), FONT_FAMILY)
    rFont.set(qn('w:cs'), FONT_FAMILY)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '27')  # 13.5 pt
    rPr.append(rFont)
    rPr.append(sz)
    r.append(rPr)
    fldSimple.append(r)
    p._p.append(fldSimple)


class ND30Builder:
    """Builder tạo văn bản hành chính chuẩn Nghị định 30/2020/NĐ-CP (ND30_Skills)"""

    def __init__(self):
        self.doc = Document()
        self.placeholders: List[str] = []
        self._init_page_setup()

    def _init_page_setup(self):
        """Khởi tạo khổ giấy A4 và lề trang chuẩn Nghị định 30"""
        section = self.doc.sections[0]
        section.page_width = Mm(PAGE_WIDTH_MM)
        section.page_height = Mm(PAGE_HEIGHT_MM)
        section.top_margin = Mm(MARGINS_DEFAULT_MM["top"])
        section.bottom_margin = Mm(MARGINS_DEFAULT_MM["bottom"])
        section.left_margin = Mm(MARGINS_DEFAULT_MM["left"])
        section.right_margin = Mm(MARGINS_DEFAULT_MM["right"])
        add_page_number_to_header(section)

    def _track_placeholder(self, text: str, field_name: str):
        """Ghi nhận các vị trí còn để trống (placeholder) để thông báo cho người dùng"""
        if "[...]" in text or "..." in text or "Số:     " in text or "Số:      " in text:
            if field_name not in self.placeholders:
                self.placeholders.append(field_name)

    def add_header(self, agency_parent: str = "", agency_name: str = "TÊN CƠ QUAN, TỔ CHỨC", 
                   doc_code: str = "Số:      /...", location: str = "Hà Nội", 
                   date_str: str = "ngày ... tháng ... năm 202..."):
        """
        Tạo phần đầu trang: Bảng 2 cột ẩn viền
        Cột 1: Cơ quan chủ quản, Cơ quan ban hành, Dòng kẻ, Số ký hiệu
        Cột 2: Quốc hiệu, Tiêu ngữ, Dòng kẻ, Địa danh & ngày tháng
        """
        table = self.doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        remove_table_borders(table)

        table.columns[0].width = Mm(75)
        table.columns[1].width = Mm(90)

        row = table.rows[0]
        cell_l, cell_r = row.cells[0], row.cells[1]
        set_cell_margins(cell_l, top=0, bottom=0, left=0, right=50)
        set_cell_margins(cell_r, top=0, bottom=0, left=50, right=0)

        # === CỘT TRÁI ===
        p_l = cell_l.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_l.paragraph_format.space_before = Pt(0)
        p_l.paragraph_format.space_after = Pt(2)
        p_l.paragraph_format.line_spacing = 1.0

        if agency_parent:
            run_parent = p_l.add_run(agency_parent.upper() + "\n")
            run_parent.font.name = FONT_FAMILY
            run_parent.font.size = Pt(12)
            run_parent.font.bold = False

        run_agency = p_l.add_run(agency_name.upper() + "\n")
        run_agency.font.name = FONT_FAMILY
        run_agency.font.size = Pt(12)
        run_agency.font.bold = True

        # Dòng kẻ dưới tên cơ quan (khoảng 1/3 đến 1/2 độ dài)
        line_len = max(6, min(14, len(agency_name) // 3))
        run_line_l = p_l.add_run("─" * line_len + "\n")
        run_line_l.font.name = FONT_FAMILY
        run_line_l.font.size = Pt(10)
        run_line_l.font.bold = True

        run_code = p_l.add_run(doc_code)
        run_code.font.name = FONT_FAMILY
        run_code.font.size = Pt(12)
        run_code.font.bold = False
        self._track_placeholder(doc_code, "Số và ký hiệu văn bản")

        # === CỘT PHẢI ===
        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(2)
        p_r.paragraph_format.line_spacing = 1.0

        run_qh = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
        run_qh.font.name = FONT_FAMILY
        run_qh.font.size = Pt(12)
        run_qh.font.bold = True

        run_tn = p_r.add_run("Độc lập - Tự do - Hạnh phúc\n")
        run_tn.font.name = FONT_FAMILY
        run_tn.font.size = Pt(13)
        run_tn.font.bold = True

        # Dòng kẻ dưới tiêu ngữ (dài bằng dòng chữ tiêu ngữ)
        run_line_r = p_r.add_run("──────────────────────\n")
        run_line_r.font.name = FONT_FAMILY
        run_line_r.font.size = Pt(10)
        run_line_r.font.bold = True

        date_full = f"{location}, {date_str}"
        run_date = p_r.add_run(date_full)
        run_date.font.name = FONT_FAMILY
        run_date.font.size = Pt(13)
        run_date.font.italic = True
        self._track_placeholder(date_full, "Ngày, tháng, năm ban hành")

    def add_title(self, doc_type: str = "", subject: str = ""):
        """
        Thêm Tên loại văn bản và Trích yếu nội dung
        - Nếu có tên loại: Tên loại (14pt, đậm, hoa), trích yếu (13-14pt, đậm)
        - Nếu công văn (không tên loại): Trích yếu đặt dưới số ký hiệu (12pt, nghiêng)
        """
        p_space = self.doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(6)
        p_space.paragraph_format.space_after = Pt(0)

        if doc_type:
            p_type = self.doc.add_paragraph()
            p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_type.paragraph_format.space_before = Pt(6)
            p_type.paragraph_format.space_after = Pt(4)
            run_t = p_type.add_run(doc_type.upper())
            run_t.font.name = FONT_FAMILY
            run_t.font.size = Pt(14)
            run_t.font.bold = True

            if subject:
                p_sub = self.doc.add_paragraph()
                p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_sub.paragraph_format.space_before = Pt(0)
                p_sub.paragraph_format.space_after = Pt(6)

                subj_text = subject if subject.lower().startswith("về việc") else f"Về việc {subject}"
                run_s = p_sub.add_run(subj_text + "\n")
                run_s.font.name = FONT_FAMILY
                run_s.font.size = Pt(13)
                run_s.font.bold = True

                # Đường kẻ dưới trích yếu
                run_line_s = p_sub.add_run("──────────")
                run_line_s.font.name = FONT_FAMILY
                run_line_s.font.size = Pt(10)
                run_line_s.font.bold = True
        else:
            p_sub = self.doc.add_paragraph()
            p_sub.paragraph_format.space_before = Pt(6)
            p_sub.paragraph_format.space_after = Pt(12)
            prefix = "" if subject.lower().startswith("v/v") or subject.lower().startswith("về việc") else "V/v "
            run_v = p_sub.add_run(f"{prefix}{subject}")
            run_v.font.name = FONT_FAMILY
            run_v.font.size = Pt(12)
            run_v.font.italic = True

    def add_legal_bases(self, bases: List[str]):
        """Thêm các căn cứ pháp lý (Căn cứ ...;)"""
        for base in bases:
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Mm(12.7)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(base)
            run.font.name = FONT_FAMILY
            run.font.size = Pt(13)
            run.font.italic = True

    def add_decision_command(self, authority_title: str = "QUYẾT ĐỊNH:"):
        """Dòng lệnh ban hành (QUYẾT ĐỊNH:) căn giữa, đậm"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(authority_title.upper())
        run.font.name = FONT_FAMILY
        run.font.size = Pt(14)
        run.font.bold = True

    def add_article(self, article_num: str, title: str, content: str):
        """Thêm Điều (Điều 1. ..., Điều 2. ...)"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Mm(12.7)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15

        prefix = f"{article_num}. " if not article_num.endswith(".") else f"{article_num} "
        run_art = p.add_run(prefix)
        run_art.font.name = FONT_FAMILY
        run_art.font.size = Pt(13)
        run_art.font.bold = True

        if title:
            run_t = p.add_run(f"{title}\n")
            run_t.font.name = FONT_FAMILY
            run_t.font.size = Pt(13)
            run_t.font.bold = True

        run_c = p.add_run(content)
        run_c.font.name = FONT_FAMILY
        run_c.font.size = Pt(13)

    def add_paragraph_content(self, text: str, is_bold_prefix: str = "", is_italic: bool = False):
        """Thêm đoạn văn nội dung thông thường căn đều hai bên, thụt đầu dòng 1.27cm"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Mm(12.7)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15

        if is_bold_prefix:
            run_b = p.add_run(is_bold_prefix + " ")
            run_b.font.name = FONT_FAMILY
            run_b.font.size = Pt(13)
            run_b.font.bold = True

        run_t = p.add_run(text)
        run_t.font.name = FONT_FAMILY
        run_t.font.size = Pt(13)
        run_t.font.italic = is_italic

    def ensure_end_marker(self):
        """Đảm bảo có dấu kết thúc ./. ở đoạn cuối cùng"""
        if not self.doc.paragraphs:
            return
        last_p = self.doc.paragraphs[-1]
        text = last_p.text.strip()
        if text and not (text.endswith("./") or text.endswith("/.")):
            last_p.add_run(" ./.")

    def add_footer(self, recipients: List[str], signer_position: str = "GIÁM ĐỐC", 
                   signer_name: str = "[Họ và tên]", signer_sub_position: str = ""):
        """
        Tạo chân trang: Bảng 2 cột ẩn viền
        Cột 1: Nơi nhận (11pt, nghiêng/đậm tiêu đề)
        Cột 2: Chức vụ, chữ ký, họ tên người ký (13-14pt, đậm)
        """
        table = self.doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        remove_table_borders(table)

        table.columns[0].width = Mm(75)
        table.columns[1].width = Mm(90)

        row = table.rows[0]
        cell_l, cell_r = row.cells[0], row.cells[1]
        set_cell_margins(cell_l, top=100, bottom=0, left=0, right=50)
        set_cell_margins(cell_r, top=100, bottom=0, left=50, right=0)

        # === NƠI NHẬN ===
        p_l = cell_l.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_l.paragraph_format.space_before = Pt(0)
        p_l.paragraph_format.space_after = Pt(2)
        p_l.paragraph_format.line_spacing = 1.0

        run_nh = p_l.add_run("Nơi nhận:\n")
        run_nh.font.name = FONT_FAMILY
        run_nh.font.size = Pt(12)
        run_nh.font.bold = True
        run_nh.font.italic = True

        for r_item in recipients:
            prefix = "" if r_item.strip().startswith("-") else "- "
            run_rcp = p_l.add_run(f"{prefix}{r_item}\n")
            run_rcp.font.name = FONT_FAMILY
            run_rcp.font.size = Pt(11)

        # === CHỮ KÝ ===
        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(2)
        p_r.paragraph_format.line_spacing = 1.0

        if signer_sub_position:
            run_sub = p_r.add_run(signer_sub_position.upper() + "\n")
            run_sub.font.name = FONT_FAMILY
            run_sub.font.size = Pt(13)
            run_sub.font.bold = True

        run_pos = p_r.add_run(signer_position.upper() + "\n\n\n\n")
        run_pos.font.name = FONT_FAMILY
        run_pos.font.size = Pt(13)
        run_pos.font.bold = True

        run_name = p_r.add_run(signer_name)
        run_name.font.name = FONT_FAMILY
        run_name.font.size = Pt(13)
        run_name.font.bold = True
        self._track_placeholder(signer_name, "Họ và tên người ký")

    def save(self, output_path: str) -> List[str]:
        """Lưu file và trả về danh sách các trường còn thiếu/placeholder"""
        self.ensure_end_marker()
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        self.doc.save(output_path)
        return self.placeholders


# Alias tương thích
ND30SkillsBuilder = ND30Builder


def build_sample_decision(output_path: str = "mau_quyet_dinh.docx") -> Tuple[str, List[str]]:
    """Tạo file Quyết định mẫu chuẩn thể thức Nghị định 30 (ND30_Skills)"""
    builder = ND30Builder()
    builder.add_header(
        agency_parent="ỦY BAN NHÂN DÂN THÀNH PHỐ HỒ CHÍ MINH",
        agency_name="SỞ NỘI VỤ",
        doc_code="Số: [...]/QĐ-SNV",
        location="Thành phố Hồ Chí Minh",
        date_str="ngày [...] tháng [...] năm 20[...]"
    )
    builder.add_title(
        doc_type="QUYẾT ĐỊNH",
        subject="Về việc phân công công tác cho công chức"
    )
    builder.add_legal_bases([
        "Căn cứ Luật Cán bộ, công chức ngày 13 tháng 11 năm 2008;",
        "Căn cứ Quyết định số 28/2022/QĐ-UBND ngày 5 tháng 8 năm 2022 của Ủy ban nhân dân Thành phố Hồ Chí Minh quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Sở Nội vụ;",
        "Theo đề nghị của Chánh Văn phòng Sở."
    ])
    builder.add_decision_command("QUYẾT ĐỊNH:")
    builder.add_article(
        "Điều 1", "",
        "Phân công ông [...], chuyên viên Văn phòng Sở chịu trách nhiệm theo dõi và tổng hợp công tác cải cách hành chính cơ quan."
    )
    builder.add_article(
        "Điều 2", "",
        "Quyết định này có hiệu lực thi hành kể từ ngày ký."
    )
    builder.add_article(
        "Điều 3", "",
        "Chánh Văn phòng, Trưởng các phòng chuyên môn nghiệp vụ thuộc Sở và ông [...] chịu trách nhiệm thi hành Quyết định này."
    )
    builder.add_footer(
        recipients=[
            "Như Điều 3;",
            "Lãnh đạo Sở;",
            "Lưu: VT, VP (02 bản)."
        ],
        signer_position="GIÁM ĐỐC",
        signer_name="[...]"
    )
    missing = builder.save(output_path)
    return output_path, missing


def build_sample_letter(output_path: str = "mau_cong_van.docx") -> Tuple[str, List[str]]:
    """Tạo file Công văn mẫu chuẩn thể thức Nghị định 30 (ND30_Skills)"""
    builder = ND30Builder()
    builder.add_header(
        agency_parent="ỦY BAN NHÂN DÂN THÀNH PHỐ HỒ CHÍ MINH",
        agency_name="SỞ THÔNG TIN VÀ TRUYỀN THÔNG",
        doc_code="Số: [...]/STTTT-CNTT",
        location="Thành phố Hồ Chí Minh",
        date_str="ngày [...] tháng [...] năm 20[...]"
    )
    builder.add_title(
        doc_type="",
        subject="Phối hợp triển khai chương trình chuyển đổi số Thành phố Hồ Chí Minh năm 2024"
    )
    builder.add_paragraph_content("Kính gửi: Ủy ban nhân dân thành phố Thủ Đức và các quận, huyện.", is_bold_prefix="Kính gửi:")
    builder.add_paragraph_content(
        "Thực hiện Kế hoạch số 72/KH-UBND ngày 20 tháng 1 năm 2024 của Ủy ban nhân dân Thành phố Hồ Chí Minh về việc triển khai chương trình chuyển đổi số và xây dựng đô thị thông minh; Sở Thông tin và Truyền thông tổ chức hội nghị tập huấn bồi dưỡng kỹ năng số cho cán bộ, công chức, viên chức trên địa bàn Thành phố."
    )
    builder.add_paragraph_content(
        "Để hội nghị tập huấn đạt kết quả tốt, Sở Thông tin và Truyền thông đề nghị Ủy ban nhân dân thành phố Thủ Đức và các quận, huyện cử đại biểu tham dự đúng thành phần và thời gian theo thông báo kèm theo."
    )
    builder.add_paragraph_content("Trân trọng cảm ơn sự phối hợp của Quý cơ quan.")
    builder.add_footer(
        recipients=[
            "Như trên;",
            "UBND Thành phố (để b/c);",
            "Giám đốc Sở;",
            "Lưu: VT, CNTT."
        ],
        signer_position="GIÁM ĐỐC",
        signer_name="[...]"
    )
    missing = builder.save(output_path)
    return output_path, missing


def standardize_docx(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Chuẩn hóa file .docx có sẵn theo Nghị định 30:
    - BẢO TOÀN FILE GỐC: Tuyệt đối không lưu đè lên input_path.
    - Tự động sinh output_path dạng: [tên_gốc]_chuan_ND30.docx nếu không chỉ định.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Không tìm thấy file: {input_path}")

    if input_path.lower().endswith(".doc"):
        raise ValueError("File định dạng .doc cũ. Vui lòng mở bằng Word và Save As sang .docx trước khi chuẩn hóa.")

    if not output_path or os.path.abspath(input_path) == os.path.abspath(output_path):
        output_path = get_standard_output_path(input_path, ".docx")

    doc = Document(input_path)

    # 1. Chuẩn hóa khổ giấy và lề trang A4
    for section in doc.sections:
        section.page_width = Mm(PAGE_WIDTH_MM)
        section.page_height = Mm(PAGE_HEIGHT_MM)
        section.top_margin = Mm(MARGINS_DEFAULT_MM["top"])
        section.bottom_margin = Mm(MARGINS_DEFAULT_MM["bottom"])
        section.left_margin = Mm(MARGINS_DEFAULT_MM["left"])
        section.right_margin = Mm(MARGINS_DEFAULT_MM["right"])
        add_page_number_to_header(section)

    # 2. Chuẩn hóa font chữ và khử lỗi dấu gạch ngang AI (—, – -> -)
    def _sanitize_paragraph(p):
        p_txt = p.text.strip()
        # Bỏ qua nếu là đường kẻ trang trí
        if p_txt and len(p_txt) >= 3 and all(c in "—–─-_ " for c in p_txt):
            return

        # Nếu là Tiêu ngữ
        if "Độc lập" in p_txt and "Tự do" in p_txt:
            for r in p.runs:
                r.font.name = FONT_FAMILY
            if len(p.runs) == 1:
                p.runs[0].text = sanitize_dashes(p.runs[0].text)
            else:
                for r in p.runs:
                    if r.text and ("—" in r.text or "–" in r.text):
                        r.text = r.text.replace("—", "-").replace("–", "-")
            return

        for r in p.runs:
            r.font.name = FONT_FAMILY
            if r.text and ("—" in r.text or "–" in r.text):
                r.text = sanitize_dashes(r.text)

    for p in doc.paragraphs:
        _sanitize_paragraph(p)

    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    _sanitize_paragraph(p)

    # 3. Chuẩn hóa giãn dòng và căn lề cho các đoạn nội dung chính
    for p in doc.paragraphs:
        text = p.text.strip()
        if text and len(text) > 40:
            if p.alignment != WD_ALIGN_PARAGRAPH.CENTER:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                if not p.paragraph_format.first_line_indent:
                    p.paragraph_format.first_line_indent = Mm(12.7)
            if not p.paragraph_format.line_spacing:
                p.paragraph_format.line_spacing = 1.15
            if not p.paragraph_format.space_after:
                p.paragraph_format.space_after = Pt(4)

    # 4. Đảm bảo có dấu kết thúc ở đoạn cuối
    if doc.paragraphs:
        body_paras = [p for p in doc.paragraphs if p.text.strip()]
        if body_paras:
            last_p = body_paras[-1]
            txt = last_p.text.strip()
            if not (txt.endswith("./") or txt.endswith("/.") or txt.endswith(".")):
                last_p.add_run(" ./.")

    doc.save(output_path)
    return output_path


# Alias tương thích ngược
standardize_existing_docx = standardize_docx


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--format":
        if len(sys.argv) < 3:
            print("Sử dụng: python builder_docx.py --format <duong_dan_file_goc.docx> [file_dich.docx]")
            sys.exit(1)
        src_file = sys.argv[2]
        dest_file = sys.argv[3] if len(sys.argv) > 3 else None
        try:
            res_file = standardize_docx(src_file, dest_file)
            print(f"🛡️ File gốc được giữ nguyên: {src_file}")
            print(f"✅ Đã tạo bản sao chuẩn hóa: {res_file}")
        except Exception as exc:
            print(f"❌ Lỗi: {exc}")
            sys.exit(1)
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "output_quyet_dinh.docx"
        target_path, missing_fields = build_sample_decision(out)
        print(f"✅ Đã tạo văn bản chuẩn thể thức: {target_path}")
        if missing_fields:
            print("⚠️ Các trường cần bổ sung thông tin:")
            for m in missing_fields:
                print(f"  - {m}")
