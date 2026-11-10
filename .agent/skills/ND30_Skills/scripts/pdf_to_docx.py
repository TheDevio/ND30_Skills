"""
Module Số hóa văn bản hành chính từ file PDF sang Word (.docx) chuẩn Nghị định 30/2020/NĐ-CP
Nguyên tắc:
1. BẢO TOÀN FILE GỐC: Tuyệt đối không thay đổi file PDF gốc.
2. TÁI SINH THỂ THỨC: Bóc tách nội dung thuần túy, không dùng text-box chắp vá,
   mà đưa dữ liệu vào ND30Builder để tạo ra file Word sạch sẽ, chuẩn 100%.
3. TỰ THẨM ĐỊNH: Tự động chạy validate_docx.py để đảm bảo file .docx tạo ra đạt 100% chuẩn thể thức.
"""

import os
import sys
import re
from typing import Dict, Any, Tuple, Optional

# Import các hằng số và quy chuẩn dùng chung
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from constants import (
    setup_windows_encoding,
    DOC_TYPE_ACCENT_MAP,
    strip_accents,
    get_standard_output_path
)

setup_windows_encoding()

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ Cần cài đặt PyMuPDF: pip install PyMuPDF")
    sys.exit(1)

from builder_docx import ND30Builder, ND30SkillsBuilder
from validate_docx import ND30Validator, ND30SkillsValidator


class ND30PDFParser:
    """Bộ bóc tách cấu trúc văn bản hành chính từ file PDF (ND30_Skills)"""

    def __init__(self, input_path: str):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Không tìm thấy file PDF: {input_path}")
        self.input_path = os.path.abspath(input_path)
        self.doc = fitz.open(self.input_path)
        self.raw_text = self._extract_raw_text()

    def _extract_raw_text(self) -> str:
        """Trích xuất toàn bộ text từ các trang PDF"""
        pages_text = []
        for page in self.doc:
            t = page.get_text()
            if t.strip():
                pages_text.append(t)
        return "\n".join(pages_text)

    def parse_components(self) -> Dict[str, Any]:
        """Phân tích các thành phần hành chính chuẩn Nghị định 30"""
        lines = [line.strip() for line in self.raw_text.splitlines() if line.strip()]

        data = {
            "agency_parent": "",
            "agency_name": "",
            "doc_code": "Số:      /...",
            "location": "Hà Nội",
            "date_str": "ngày ... tháng ... năm 202...",
            "doc_type": "",
            "subject": "",
            "legal_bases": [],
            "command": "",
            "articles": [],
            "body_paragraphs": [],
            "recipients": [],
            "signer_position": "",
            "signer_name": "[Họ và tên]"
        }

        # 1. Trích xuất Địa danh, Ngày tháng năm
        date_match = re.search(
            r"([A-Za-zÀ-ỹ\s]+),\s*ngày\s+(\d{1,2}|\.+)\s+tháng\s+(\d{1,2}|\.+)\s+năm\s+(\d{4}|\.+)", 
            self.raw_text, re.IGNORECASE
        )
        if date_match:
            data["location"] = date_match.group(1).strip()
            day = date_match.group(2).lstrip("0") if date_match.group(2).isdigit() else date_match.group(2)
            month = date_match.group(3).lstrip("0") if date_match.group(3).isdigit() else date_match.group(3)
            year = date_match.group(4)
            data["date_str"] = f"ngày {day} tháng {month} năm {year}"

        # 2. Trích xuất Số, ký hiệu
        code_match = re.search(r"Số:\s*([0-9a-zA-Z\./\-_]+)", self.raw_text, re.IGNORECASE)
        if code_match:
            data["doc_code"] = f"Số: {code_match.group(1)}"

        # 3. Trích xuất Tên cơ quan ban hành / cấp trên
        for l in lines[:10]:
            upper = l.upper()
            if any(k in upper for k in ["ỦY BAN NHÂN DÂN", "BỘ ", "SỞ ", "TỔNG CÔNG TY", "CÔNG TY", "HỌC VIỆN", "TRƯỜNG ĐẠI HỌC", "BAN "]):
                if "CỘNG HÒA" not in upper and "ĐỘC LẬP" not in upper:
                    if not data["agency_parent"] and any(k in upper for k in ["ỦY BAN NHÂN DÂN TỈNH", "BỘ ", "TỔNG CÔNG TY"]):
                        data["agency_parent"] = l
                    elif not data["agency_name"]:
                        data["agency_name"] = l

        if not data["agency_name"]:
            data["agency_name"] = data["agency_parent"] if data["agency_parent"] else "TÊN CƠ QUAN, TỔ CHỨC"
            if data["agency_parent"] == data["agency_name"]:
                data["agency_parent"] = ""

        # 4. Trích xuất Tên loại văn bản & Trích yếu (Hỗ trợ Unicode và không dấu/lỗi font)
        for i, l in enumerate(lines[:30]):
            clean_l = strip_accents(l.upper()).strip()
            alpha_only = re.sub(r"[^A-Z\s]", "", clean_l).strip()

            matched_type = None
            for key, val in DOC_TYPE_ACCENT_MAP.items():
                if alpha_only == key or key in alpha_only or (key == "QUYET DINH" and "QUY" in alpha_only and "NH" in alpha_only):
                    matched_type = val
                    break

            if matched_type:
                data["doc_type"] = matched_type
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    clean_next = strip_accents(next_line.lower())
                    if "ve viec" in clean_next or "v/v" in clean_next or len(next_line) > 10:
                        data["subject"] = next_line
                break

        # Nếu không có tên loại văn bản viết hoa riêng, tìm trích yếu V/v
        if not data["subject"]:
            subj_match = re.search(r"(V/v|Về việc)\s+([^\n\.;]+)", self.raw_text, re.IGNORECASE)
            if subj_match:
                data["subject"] = subj_match.group(0).strip()
            elif data["doc_type"]:
                data["subject"] = f"Về việc ban hành văn bản {data['doc_type'].lower()}"

        # 5. Trích xuất Căn cứ pháp lý
        for l in lines:
            clean_l = strip_accents(l.strip())
            if clean_l.startswith("Can cu") or clean_l.startswith("Theo de nghi") or l.strip().startswith("Căn cứ") or l.strip().startswith("Theo đề nghị"):
                data["legal_bases"].append(l.strip())

        # 6. Trích xuất Điều khoản (Điều 1, Điều 2...) hoặc Đoạn văn nội dung
        current_article = None
        for l in lines:
            art_match = re.match(r"^(Điều\s+\d+)[\.:\s]+(.*)$", l, re.IGNORECASE)
            if art_match:
                if current_article:
                    data["articles"].append(current_article)
                current_article = {
                    "num": art_match.group(1).title(),
                    "title": "",
                    "content": art_match.group(2).strip()
                }
            elif current_article:
                if not l.startswith("Nơi nhận") and not l.startswith("TM.") and not l.startswith("KT."):
                    current_article["content"] += " " + l.strip()
                else:
                    data["articles"].append(current_article)
                    current_article = None

        if current_article:
            data["articles"].append(current_article)

        # 7. Trích xuất Nơi nhận
        recipients_found = False
        for l in lines:
            if "Nơi nhận:" in l or "Nơi nhận" in l:
                recipients_found = True
                continue
            if recipients_found:
                if any(pos in l.upper() for pos in ["GIÁM ĐỐC", "CHỦ TỊCH", "HIỆU TRƯỞNG", "TỔNG GIÁM ĐỐC", "KT.", "TM."]):
                    break
                if l.startswith("-") or l.startswith("•"):
                    data["recipients"].append(l.lstrip("-• ").strip())
                elif l.strip().startswith("Lưu:"):
                    data["recipients"].append(l.strip())

        if not data["recipients"]:
            data["recipients"] = ["Như trên;", "Lưu: VT, HCTH."]

        # 8. Trích xuất Người ký & Chức vụ
        for l in lines[-15:]:
            upper = l.upper()
            if any(pos in upper for pos in ["GIÁM ĐỐC", "CHỦ TỊCH", "HIỆU TRƯỞNG", "TỔNG GIÁM ĐỐC", "TRƯỞNG PHÒNG"]):
                data["signer_position"] = l.upper()
            elif data["signer_position"] and len(l.split()) >= 2 and l.istitle():
                data["signer_name"] = l.strip()

        return data


# Alias tương thích
ND30SkillsPDFParser = ND30PDFParser
AdministrativePDFParser = ND30PDFParser


def convert_pdf_to_docx(input_path: str, output_path: Optional[str] = None) -> Tuple[str, bool]:
    """
    Số hóa file PDF sang file Word (.docx) đạt chuẩn 100% Nghị định 30 (ND30_Skills):
    - BẢO TOÀN FILE GỐC: Tuyệt đối không thay đổi file PDF gốc.
    - Tự động sinh output_path dạng: [tên_gốc]_chuan_ND30.docx nếu không chỉ định.
    - Tự động chạy bộ thẩm định thể thức chuyên sâu.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Không tìm thấy file: {input_path}")

    if not output_path:
        output_path = get_standard_output_path(input_path, ".docx")

    print(f"\n{'='*70}")
    print(f"  SỐ HÓA VĂN BẢN TỪ PDF SANG WORD CHUẨN NGHỊ ĐỊNH 30/2020/NĐ-CP (ND30_Skills)")
    print(f"  File PDF gốc (Bảo toàn 100%): {os.path.basename(input_path)}")
    print(f"  File Word đích sẽ tạo:       {os.path.basename(output_path)}")
    print(f"{'='*70}\n")

    # 1. Bóc tách dữ liệu từ PDF
    print("⏳ Bước 1: Trích xuất cấu trúc văn bản từ PDF...")
    parser = ND30PDFParser(input_path)
    data = parser.parse_components()

    # 2. Dựng lại văn bản bằng ND30Builder
    print("⏳ Bước 2: Dựng lại văn bản Word theo khuôn thể thức Nghị định 30...")
    builder = ND30Builder()

    builder.add_header(
        agency_parent=data["agency_parent"],
        agency_name=data["agency_name"],
        doc_code=data["doc_code"],
        location=data["location"],
        date_str=data["date_str"]
    )

    builder.add_title(
        doc_type=data["doc_type"] if data["doc_type"] else "VĂN BẢN",
        subject=data["subject"]
    )

    if data["legal_bases"]:
        builder.add_legal_bases(data["legal_bases"])

    if data["doc_type"] == "QUYẾT ĐỊNH":
        builder.add_decision_command("QUYẾT ĐỊNH:")

    if data["articles"]:
        for art in data["articles"]:
            builder.add_article(art["num"], art.get("title", ""), art["content"])
    else:
        body_lines = [l for l in parser.raw_text.splitlines() if len(l.strip()) > 35]
        for bl in body_lines[:15]:
            builder.add_paragraph_content(bl.strip())

    builder.add_footer(
        recipients=data["recipients"],
        signer_position=data["signer_position"] if data["signer_position"] else "GIÁM ĐỐC",
        signer_name=data["signer_name"]
    )

    missing = builder.save(output_path)
    print(f"✅ Đã tạo file Word: {output_path}")

    # 3. Tự thẩm định bằng bộ kiểm tra thể thức tự động
    print("\n⏳ Bước 3: Chạy bộ thẩm định thể thức trên file Word vừa sinh...")
    validator = ND30Validator(output_path)
    is_valid = validator.run_all()
    validator.print_report()

    if missing:
        print("⚠️ Các vị trí để trống bạn cần điền hoàn thiện:")
        for m in missing:
            print(f"  - {m}")

    return output_path, is_valid


# Alias tương thích ngược
convert_pdf_to_docx_nd30 = convert_pdf_to_docx


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python pdf_to_docx.py <duong_dan_file.pdf> [file_dich.docx]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    docx_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        out_doc, ok = convert_pdf_to_docx(pdf_file, docx_file)
        sys.exit(0 if ok else 1)
    except Exception as exc:
        print(f"❌ Lỗi: {exc}")
        sys.exit(1)
