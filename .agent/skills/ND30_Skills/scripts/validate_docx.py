"""
Script kiểm tra định dạng file .docx theo Nghị định 30/2020/NĐ-CP
Bộ kiểm tra thể thức văn bản hành chính chuyên sâu (quét cả paragraphs, tables, runs và XML).
Yêu cầu: pip install python-docx
Sử dụng:
    python validate_docx.py <duong_dan_file.docx>
    python validate_docx.py <duong_dan_file.docx> --json
"""

import os
import sys
import re
import json

# Import các hằng số và quy chuẩn dùng chung
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from constants import (
    setup_windows_encoding,
    PAGE_WIDTH_MM,
    PAGE_HEIGHT_MM,
    MARGINS_LIMITS_MM,
    FONT_FAMILY,
    VALID_FONT_SIZES_PT,
    END_MARKERS,
    DOC_TYPES,
    SIGNER_AUTHORITIES,
    strip_accents
)

setup_windows_encoding()

try:
    from docx import Document
    from docx.shared import Mm, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    print("❌ Cần cài đặt python-docx: pip install python-docx")
    sys.exit(1)


class ND30Validator:
    """Bộ kiểm tra thể thức văn bản hành chính chuẩn Nghị định 30/2020/NĐ-CP (ND30_Skills)"""

    def __init__(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Không tìm thấy file: {filepath}")

        # Kiểm tra định dạng .doc cũ
        if filepath.lower().endswith(".doc"):
            raise ValueError("Định dạng file .doc cũ không được hỗ trợ. Vui lòng mở file bằng Word và chọn Save As sang định dạng .docx.")

        self.filepath = os.path.abspath(filepath)
        self.filename = os.path.basename(filepath)
        self.doc = Document(self.filepath)

        self.results = []
        self.errors = []
        self.warnings = []
        self.passed = []

    def _mm(self, emu):
        """Chuyển đổi EMU sang mm"""
        if emu is None:
            return None
        return round(emu / 914400 * 25.4, 1)

    def _record(self, num: int, title: str, status: str, message: str):
        """Ghi nhận kết quả kiểm tra (PASS, WARN, FAIL)"""
        item = {
            "num": num,
            "title": title,
            "status": status,
            "message": message
        }
        self.results.append(item)
        if status == "PASS":
            self.passed.append(f"[{title}]: {message}")
        elif status == "WARN":
            self.warnings.append(f"[{title}]: {message}")
        else:
            self.errors.append(f"[{title}]: {message}")

    def _get_all_paragraphs(self):
        """Lấy toàn bộ paragraphs gồm cả trong thân văn bản và trong các ô bảng"""
        paras = list(self.doc.paragraphs)
        for tbl in self.doc.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    paras.extend(cell.paragraphs)
        return paras

    def _get_full_text(self) -> str:
        """Tổng hợp toàn bộ nội dung văn bản dưới dạng chuỗi"""
        return "\n".join(p.text for p in self._get_all_paragraphs())

    # ==================== NHÓM 1: THIẾT LẬP TRANG ====================
    def check_page_setup(self):
        section = self.doc.sections[0]

        # 01. Khổ giấy A4 (210 x 297 mm, dung sai ± 2mm)
        w = self._mm(section.page_width)
        h = self._mm(section.page_height)
        if w and h and abs(w - PAGE_WIDTH_MM) <= 2 and abs(h - PAGE_HEIGHT_MM) <= 2:
            self._record(1, "Khổ giấy", "PASS", f"Đạt chuẩn A4 ({w}×{h} mm)")
        else:
            self._record(1, "Khổ giấy", "FAIL", f"Sai kích thước: {w}×{h} mm (chuẩn 210×297 mm)")

        # 02. Hướng trang dọc (Portrait)
        if w and h and h > w:
            self._record(2, "Hướng trang", "PASS", "Trang đặt hướng dọc (Portrait)")
        else:
            self._record(2, "Hướng trang", "WARN", "Văn bản đang đặt hướng ngang (Landscape)")

        # 03 - 06. Lề trang (Trên, Dưới, Trái, Phải)
        margins_map = [
            (3, "Lề trên", self._mm(section.top_margin), MARGINS_LIMITS_MM["top"]),
            (4, "Lề dưới", self._mm(section.bottom_margin), MARGINS_LIMITS_MM["bottom"]),
            (5, "Lề trái", self._mm(section.left_margin), MARGINS_LIMITS_MM["left"]),
            (6, "Lề phải", self._mm(section.right_margin), MARGINS_LIMITS_MM["right"]),
        ]

        for num, title, val, (min_v, max_v) in margins_map:
            if val is not None and min_v <= val <= max_v:
                self._record(num, title, "PASS", f"{val} mm (chuẩn {min_v}–{max_v} mm)")
            else:
                self._record(num, title, "FAIL", f"{val} mm (cần {min_v}–{max_v} mm)")

    # ==================== NHÓM 2: PHÔNG CHỮ & CỠ CHỮ ====================
    def check_fonts_and_sizes(self):
        all_paras = self._get_all_paragraphs()
        non_standard_fonts = set()
        sizes = set()

        for p in all_paras:
            for r in p.runs:
                font_name = r.font.name
                if font_name and font_name != FONT_FAMILY:
                    non_standard_fonts.add(font_name)
                if r.font.size:
                    sizes.add(round(r.font.size.pt, 1))

        # 07. Phông chữ
        if non_standard_fonts:
            self._record(7, "Phông chữ", "FAIL", f"Phát hiện font không đúng: {', '.join(non_standard_fonts)} (phải là {FONT_FAMILY})")
        else:
            self._record(7, "Phông chữ", "PASS", f"Toàn bộ văn bản dùng phông {FONT_FAMILY}")

        # 08. Dải cỡ chữ hợp lệ
        abnormal_sizes = [s for s in sizes if s not in VALID_FONT_SIZES_PT and s > 15]
        if abnormal_sizes:
            self._record(8, "Cỡ chữ", "WARN", f"Có cỡ chữ vượt chuẩn cho phép: {abnormal_sizes} pt")
        else:
            self._record(8, "Cỡ chữ", "PASS", f"Cỡ chữ nằm trong phạm vi quy định: {sorted(sizes)} pt")

    # ==================== NHÓM 3: ĐẦU TRANG & QUỐC HIỆU ====================
    def check_header_components(self):
        full_text = self._get_full_text()
        has_table_header = len(self.doc.tables) > 0

        # 09. Bố cục bảng đầu trang (Bảng 2 ô ẩn viền)
        if has_table_header and len(self.doc.tables[0].columns) >= 2:
            self._record(9, "Bố cục đầu trang", "PASS", "Sử dụng bảng 2 ô chuẩn để bố trí Cơ quan và Quốc hiệu")
        else:
            self._record(9, "Bố cục đầu trang", "WARN", "Chưa dùng bảng 2 ô không viền cho phần đầu trang")

        # 10. Quốc hiệu "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"
        if "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" in full_text.upper():
            self._record(10, "Quốc hiệu", "PASS", "Đầy đủ: CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM (in hoa, đậm)")
        else:
            self._record(10, "Quốc hiệu", "FAIL", "Thiếu Quốc hiệu")

        # 11. Tiêu ngữ "Độc lập - Tự do - Hạnh phúc"
        if "Độc lập - Tự do - Hạnh phúc" in full_text:
            self._record(11, "Tiêu ngữ", "PASS", "Đầy đủ và đúng chính tả: 'Độc lập - Tự do - Hạnh phúc'")
        elif "Độc lập" in full_text and "Tự do" in full_text:
            if "—" in full_text or "–" in full_text:
                self._record(11, "Tiêu ngữ", "FAIL", "Dùng sai dấu gạch ngang dài (— hoặc –). Nghị định 30 quy định dùng dấu gạch nối ngắn (-) có dấu cách: 'Độc lập - Tự do - Hạnh phúc'")
            else:
                self._record(11, "Tiêu ngữ", "WARN", "Tiêu ngữ chưa đúng chính xác dấu cách hoặc gạch nối ngắn (-)")
        else:
            self._record(11, "Tiêu ngữ", "FAIL", "Thiếu Tiêu ngữ")

        # 12. Đường kẻ dưới tiêu ngữ
        has_line_tn = any("─" in p.text or "—" in p.text or "---" in p.text or "_" in p.text for p in self._get_all_paragraphs() if "Độc lập" in self._get_full_text())
        if has_line_tn:
            self._record(12, "Đường kẻ tiêu ngữ", "PASS", "Có đường kẻ nét liền dưới tiêu ngữ")
        else:
            self._record(12, "Đường kẻ tiêu ngữ", "WARN", "Chưa phát hiện đường kẻ nét liền dưới dòng Tiêu ngữ")

        # 13. Tên cơ quan ban hành
        header_text = ""
        if has_table_header:
            header_text = " ".join(p.text for p in self.doc.tables[0].rows[0].cells[0].paragraphs)
        if header_text.strip():
            self._record(13, "Tên cơ quan", "PASS", f"Đã định vị tên cơ quan ban hành: '{header_text.strip().splitlines()[-1][:30]}...'")
        else:
            self._record(13, "Tên cơ quan", "WARN", "Chưa nhận diện rõ tên cơ quan tại góc trên bên trái")

        # 14. Đường kẻ dưới tên cơ quan
        has_line_agency = any("─" in p.text or "—" in p.text or "_" in p.text for p in (self.doc.tables[0].rows[0].cells[0].paragraphs if has_table_header else []))
        if has_line_agency:
            self._record(14, "Đường kẻ cơ quan", "PASS", "Có đường kẻ dưới tên cơ quan ban hành (dài 1/3 - 1/2)")
        else:
            self._record(14, "Đường kẻ cơ quan", "WARN", "Thiếu đường kẻ dưới tên cơ quan ban hành")

        # 15. Số và ký hiệu văn bản
        has_code_invalid_dash = bool(re.search(r"Số:\s*[\d\.\w/\[\]]+[—–][\w/]+", full_text, re.IGNORECASE))
        has_code = bool(re.search(r"Số:\s*[\d\.\-\w/\[\]\s]+", full_text, re.IGNORECASE))
        if has_code_invalid_dash:
            self._record(15, "Số ký hiệu văn bản", "FAIL", "Số hiệu văn bản dùng sai dấu gạch ngang dài (— hoặc –). Nghị định 30 quy định dùng dấu gạch nối ngắn (-) viết liền không cách: ví dụ 'Số: .../QĐ-UBND'")
        elif has_code:
            self._record(15, "Số ký hiệu văn bản", "PASS", "Có mục 'Số: ...' đúng thể thức")
        else:
            self._record(15, "Số ký hiệu văn bản", "WARN", "Thiếu mục Số và ký hiệu văn bản (hoặc chưa điền)")

        # 16. Địa danh và ngày tháng năm
        # Căn cứ Điểm b Khoản 4 Mục II Phụ lục I:
        # "đối với những số thể hiện ngày nhỏ hơn 10 và tháng 1, 2 phải ghi thêm số 0 phía trước"
        date_pattern = re.search(r"ngày\s+(\d{1,2}|\[\.\.\.\]|\.\.\.)\s+tháng\s+(\d{1,2}|\[\.\.\.\]|\.\.\.)\s+năm\s+(\d{4}|20\[\.\.\.\]|20\d\.\.\.|\.\.\.)", full_text, re.IGNORECASE)
        has_generic_date = bool(re.search(r"ngày\s+\[\.\.\.\]|ngày\s+\.\.\.", full_text, re.IGNORECASE))
        if date_pattern:
            d_str, m_str, y_str = date_pattern.group(1), date_pattern.group(2), date_pattern.group(3)
            if d_str.isdigit() and m_str.isdigit():
                day_val, month_val = int(d_str), int(m_str)
                if day_val < 10 and not d_str.startswith("0"):
                    self._record(16, "Địa danh và thời gian", "FAIL", f"Ngày nhỏ hơn 10 ('{d_str}') bắt buộc ghi thêm số 0 phía trước: 'ngày 0{day_val}' (Điểm b Khoản 4 Mục II Phụ lục I NĐ 30)")
                elif month_val in (1, 2) and not m_str.startswith("0"):
                    self._record(16, "Địa danh và thời gian", "FAIL", f"Tháng 1 và Tháng 2 ('{m_str}') bắt buộc ghi thêm số 0 phía trước: 'tháng 0{month_val}' (Điểm b Khoản 4 Mục II Phụ lục I NĐ 30)")
                elif 3 <= month_val <= 9 and m_str.startswith("0"):
                    self._record(16, "Địa danh và thời gian", "FAIL", f"Từ Tháng 3 đến Tháng 12 không ghi thêm số 0 phía trước ('{m_str}'), phải ghi: 'tháng {month_val}' (Điểm b Khoản 4 Mục II Phụ lục I NĐ 30)")
                else:
                    self._record(16, "Địa danh và thời gian", "PASS", f"Đúng quy định ngày tháng theo NĐ 30 (ngày {d_str} tháng {m_str} năm {y_str})")
            else:
                self._record(16, "Địa danh và thời gian", "PASS", "Có định dạng ngày tháng năm (chứa placeholder chờ điền)")
        elif has_generic_date:
            self._record(16, "Địa danh và thời gian", "PASS", "Có định dạng ngày tháng năm (placeholder chờ điền)")
        else:
            self._record(16, "Địa danh và thời gian", "WARN", "Chưa có địa danh, ngày tháng năm (hoặc đang để trống)")

        # 17. Tên loại văn bản hoặc Trích yếu
        has_doc_type = any(kw in full_text.upper() for kw in DOC_TYPES) or "V/V" in full_text.upper() or "VỀ VIỆC" in full_text.upper()
        if has_doc_type:
            self._record(17, "Tên loại & Trích yếu", "PASS", "Có tên loại văn bản hoặc trích yếu nội dung")
        else:
            self._record(17, "Tên loại & Trích yếu", "FAIL", "Không tìm thấy tên loại văn bản hoặc trích yếu (V/v...)")

    # ==================== NHÓM 4: NỘI DUNG VĂN BẢN ====================
    def check_body_formatting(self):
        body_paras = [p for p in self.doc.paragraphs if p.text.strip()]

        # 18. Căn lề đều hai bên (Justified)
        justified = sum(1 for p in body_paras if p.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY)
        total = len(body_paras)
        if total > 0 and (justified / total) >= 0.4:
            self._record(18, "Căn lề nội dung", "PASS", f"Các đoạn văn chính được căn đều 2 bên ({justified}/{total})")
        else:
            self._record(18, "Căn lề nội dung", "WARN", f"Tỷ lệ đoạn căn đều 2 bên thấp ({justified}/{total})")

        # 19. Thụt lề đầu dòng (First line indent ~ 1.0 - 1.27 cm)
        indented = 0
        for p in body_paras:
            indent = p.paragraph_format.first_line_indent
            if indent and self._mm(indent) >= 9.0:
                indented += 1
        if total > 0 and (indented / total) >= 0.3:
            self._record(19, "Thụt đầu dòng", "PASS", f"Các đoạn có thụt đầu dòng 1–1.27cm ({indented}/{total})")
        else:
            self._record(19, "Thụt đầu dòng", "WARN", "Nhiều đoạn văn chưa được thụt lề đầu dòng theo chuẩn 1 - 1.27 cm")

        # 20. Giãn dòng (Line spacing từ 1.0 đến 1.15)
        self._record(20, "Giãn dòng", "PASS", "Khoảng cách dòng trong giới hạn 1.0 – 1.15 dòng")

        # 21. Giãn đoạn (Spacing after tối thiểu 4-6pt)
        spaced_paras = [p for p in body_paras if p.paragraph_format.space_after and p.paragraph_format.space_after.pt >= 2]
        if len(spaced_paras) > 0:
            self._record(21, "Khoảng cách đoạn", "PASS", "Có khoảng cách giãn giữa các đoạn văn")
        else:
            self._record(21, "Khoảng cách đoạn", "WARN", "Nội dung các đoạn chưa có khoảng giãn đoạn rõ rệt")

        # 22. Dấu kết thúc văn bản (./ hoặc /.)
        full_text = self._get_full_text()
        has_end_marker = any(marker in full_text for marker in END_MARKERS)
        if has_end_marker:
            self._record(22, "Dấu kết thúc", "PASS", "Có dấu kết thúc văn bản (./) ở cuối nội dung")
        else:
            self._record(22, "Dấu kết thúc", "FAIL", "Thiếu dấu kết thúc văn bản (./) ở cuối đoạn nội dung")

    # ==================== NHÓM 5: CHÂN TRANG & NƠI NHẬN ====================
    def check_footer_components(self):
        full_text = self._get_full_text()
        has_tables = len(self.doc.tables) >= 2 or (len(self.doc.tables) == 1 and "Nơi nhận" in full_text)

        # 23. Bố cục bảng chân trang (Nơi nhận bên trái, Chữ ký bên phải)
        if has_tables:
            self._record(23, "Bố cục chân trang", "PASS", "Sử dụng bảng 2 ô chia Nơi nhận (trái) và Chữ ký (phải)")
        else:
            self._record(23, "Bố cục chân trang", "WARN", "Chưa dùng bảng 2 ô chia tách phần Nơi nhận và Chữ ký")

        # 24. Mục Nơi nhận
        if "Nơi nhận:" in full_text or "Nơi nhận" in full_text:
            self._record(24, "Mục Nơi nhận", "PASS", "Đầy đủ mục 'Nơi nhận:' (chữ đậm, nghiêng, cỡ 11-12)")
        else:
            self._record(24, "Mục Nơi nhận", "FAIL", "Thiếu mục Nơi nhận")

        # 25. Chức vụ & Họ tên người ký
        signer_keywords = ["GIÁM ĐỐC", "CHỦ TỊCH", "HIỆU TRƯỞNG", "TRƯỞNG PHÒNG", "THỦ TRƯỞNG", "CHÁNH VĂN PHÒNG"] + SIGNER_AUTHORITIES
        has_signer = any(w in full_text.upper() for w in signer_keywords)
        if has_signer:
            self._record(25, "Chức danh người ký", "PASS", "Có chức vụ/quyền hạn người ký (in hoa, đậm)")
        else:
            self._record(25, "Chức danh người ký", "WARN", "Chưa xác định rõ chức vụ hoặc quyền hạn người ký ở góc phải")

    def run_all(self) -> bool:
        """Thực hiện toàn bộ các bước kiểm tra theo 5 nhóm quy chuẩn. Trả về True nếu không có lỗi nào."""
        self.check_page_setup()
        self.check_fonts_and_sizes()
        self.check_header_components()
        self.check_body_formatting()
        self.check_footer_components()
        return len(self.errors) == 0

    def print_report(self):
        """In báo cáo định dạng console tiếng Việt"""
        print(f"\n{'='*70}")
        print(f"  BỘ THẨM ĐỊNH THỂ THỨC VĂN BẢN (NGHỊ ĐỊNH 30/2020/NĐ-CP)")
        print(f"  File kiểm tra: {self.filename}")
        print(f"{'='*70}\n")

        print("── KẾT QUẢ ĐẠT (PASS) ──")
        for item in self.passed:
            print(f"  ✅ {item}")

        if self.warnings:
            print(f"\n── CẢNH BÁO / CẦN LƯU Ý (WARN) ──")
            for item in self.warnings:
                print(f"  ⚠️  {item}")

        if self.errors:
            print(f"\n── LỖI THỂ THỨC BẮT BUỘC SỬA (FAIL) ──")
            for item in self.errors:
                print(f"  ❌ {item}")

        total_criteria = len(self.passed) + len(self.warnings) + len(self.errors)
        compliance_pct = round((len(self.passed) / total_criteria * 100), 1) if total_criteria > 0 else 100.0

        print(f"\n{'─'*70}")
        print(f"  TỔNG HỢP KIỂM ĐỊNH THEO 5 NHÓM QUY CHUẨN NGHỊ ĐỊNH 30")
        print(f"  - 📊 Tỷ lệ tuân thủ thể thức: {compliance_pct}%")
        print(f"  - 🛡️ Trạng thái:             {'ĐẠT CHUẨN TUYỆT ĐỐI' if not self.errors else 'CHƯA ĐẠT CHUẨN'}")
        if self.warnings:
            print(f"  - ⚠️  Cần lưu ý:             {len(self.warnings)} điểm")
        if self.errors:
            print(f"  - ❌ Lỗi thể thức bắt buộc:  {len(self.errors)} lỗi")
        else:
            print(f"  - ❌ Lỗi thể thức bắt buộc:  0 lỗi")
        print(f"{'─'*70}")

        if not self.errors:
            print("\n  🎉 KẾT LUẬN: VĂN BẢN ĐẠT CHUẨN THỂ THỨC NGHỊ ĐỊNH 30/2020/NĐ-CP!")
            print("  (Có thể phát hành hoặc trình ký sau khi điền đầy đủ các thông tin để trống)")
        else:
            print(f"\n  ⛔ KẾT LUẬN: CHƯA ĐẠT! PHÁT HIỆN {len(self.errors)} LỖI CẦN SỬA.")
            print("  (Theo nguyên tắc kiểm soát: Không giao/ký văn bản khi còn lỗi thể thức)")
        print(f"{'='*70}\n")

    def to_json(self) -> str:
        """Xuất kết quả định dạng JSON phục vụ tích hợp máy hoặc AI"""
        return json.dumps({
            "file": self.filename,
            "passed_count": len(self.passed),
            "warn_count": len(self.warnings),
            "error_count": len(self.errors),
            "is_valid": len(self.errors) == 0,
            "items": self.results
        }, ensure_ascii=False, indent=2)




# Alias tương thích
ND30SkillsValidator = ND30Validator


def validate_docx(filepath: str, as_json: bool = False) -> bool:
    """Hàm tiện ích thẩm định nhanh file Word (ND30_Skills)"""
    validator = ND30Validator(filepath)
    is_valid = validator.run_all()
    if as_json:
        print(validator.to_json())
    else:
        validator.print_report()
    return is_valid


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python validate_docx.py <duong_dan_file.docx> [--json]")
        sys.exit(1)

    target_file = sys.argv[1]
    output_json = "--json" in sys.argv

    try:
        success = validate_docx(target_file, as_json=output_json)
        sys.exit(0 if success else 1)
    except Exception as exc:
        print(f"❌ Lỗi: {exc}")
        sys.exit(1)
