"""
Các hằng số và quy chuẩn kỹ thuật theo Nghị định 30/2020/NĐ-CP
Được dùng chung thống nhất cho toàn bộ hệ thống (builder, validator, pdf parser).
"""

import os
import re
import sys
import unicodedata

# 1. Hỗ trợ hiển thị UTF-8 trên Windows Terminal
def setup_windows_encoding():
    """Thiết lập mã hóa UTF-8 cho stdout và stderr trên Windows"""
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass


# 2. Quy chuẩn khổ giấy & lề trang (Phụ lục I, NĐ 30/2020/NĐ-CP)
PAGE_WIDTH_MM = 210.0
PAGE_HEIGHT_MM = 297.0

# Lề mặc định khi tạo mới (mm)
MARGINS_DEFAULT_MM = {
    "top": 20.0,
    "bottom": 20.0,
    "left": 30.0,
    "right": 20.0
}

# Giới hạn cho phép của lề trang (min_mm, max_mm)
MARGINS_LIMITS_MM = {
    "top": (20.0, 25.0),
    "bottom": (20.0, 25.0),
    "left": (30.0, 35.0),
    "right": (15.0, 20.0)
}

# 3. Phông chữ và cỡ chữ
FONT_FAMILY = "Times New Roman"
VALID_FONT_SIZES_PT = {10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0}

# 4. Hậu tố đặt tên bản sao chuẩn hóa
OUTPUT_SUFFIX = "_chuan_ND30"

# 5. Dấu kết thúc văn bản
END_MARKERS = ("./", "/.")

# 6. Danh mục 29 loại văn bản hành chính theo Nghị định 30/2020/NĐ-CP (Điều 3 và Phụ lục III)
DOC_TYPES = [
    "NGHỊ QUYẾT",
    "QUYẾT ĐỊNH",
    "CHỈ THỊ",
    "QUY CHẾ",
    "QUY ĐỊNH",
    "THÔNG CÁO",
    "THÔNG BÁO",
    "HƯỚNG DẪN",
    "CHƯƠNG TRÌNH",
    "KẾ HOẠCH",
    "PHƯƠNG ÁN",
    "ĐỀ ÁN",
    "DỰ ÁN",
    "BÁO CÁO",
    "BIÊN BẢN",
    "TỜ TRÌNH",
    "HỢP ĐỒNG",
    "CÔNG VĂN",
    "CÔNG ĐIỆN",
    "BẢN GHI NHỚ",
    "BẢN THỎA THUẬN",
    "GIẤY ỦY QUYỀN",
    "GIẤY MỜI",
    "GIẤY GIỚI THIỆU",
    "GIẤY NGHỈ PHÉP",
    "PHIẾU GỬI",
    "PHIẾU CHUYỂN",
    "PHIẾU BÁO",
    "THƯ CÔNG"
]

# Bảng chữ viết tắt tên loại văn bản hành chính (Mục I, Phụ lục III, Nghị định 30/2020/NĐ-CP)
DOC_TYPE_ABBREVIATIONS = {
    "NGHỊ QUYẾT": "NQ",
    "QUYẾT ĐỊNH": "QĐ",
    "CHỈ THỊ": "CT",
    "QUY CHẾ": "QC",
    "QUY ĐỊNH": "QyĐ",
    "THÔNG CÁO": "TC",
    "THÔNG BÁO": "TB",
    "HƯỚNG DẪN": "HD",
    "CHƯƠNG TRÌNH": "CTr",
    "KẾ HOẠCH": "KH",
    "PHƯƠNG ÁN": "PA",
    "ĐỀ ÁN": "ĐA",
    "DỰ ÁN": "DA",
    "BÁO CÁO": "BC",
    "BIÊN BẢN": "BB",
    "TỜ TRÌNH": "TTr",
    "HỢP ĐỒNG": "HĐ",
    "CÔNG VĂN": "",       # Công văn không có chữ viết tắt tên loại trong số ký hiệu
    "CÔNG ĐIỆN": "CĐ",
    "BẢN GHI NHỚ": "BGN",
    "BẢN THỎA THUẬN": "BTT",
    "GIẤY ỦY QUYỀN": "GUQ",
    "GIẤY MỜI": "GM",
    "GIẤY GIỚI THIỆU": "GGT",
    "GIẤY NGHỈ PHÉP": "GNP",
    "PHIẾU GỬI": "PG",
    "PHIẾU CHUYỂN": "PC",
    "PHIẾU BÁO": "PB",
    "THƯ CÔNG": ""
}

# Bảng chữ viết tắt các hình thức bản sao (Mục I, Phụ lục III, Nghị định 30/2020/NĐ-CP)
COPY_TYPE_ABBREVIATIONS = {
    "SAO Y": "SY",
    "TRÍCH SAO": "TrS",
    "SAO LỤC": "SL"
}

# 5 trường hợp viết tắt quyền hạn người ký (Điểm b Khoản 7 Mục II Phụ lục I)
SIGNER_AUTHORITIES = ["TM.", "Q.", "KT.", "TL.", "TUQ."]

# Bảng map không dấu sang tên chuẩn tiếng Việt (hỗ trợ OCR và PDF lỗi font nhúng)
DOC_TYPE_ACCENT_MAP = {
    "NGHI QUYET": "NGHỊ QUYẾT",
    "QUYET DINH": "QUYẾT ĐỊNH",
    "CHI THI": "CHỈ THỊ",
    "QUY CHE": "QUY CHẾ",
    "QUY DINH": "QUY ĐỊNH",
    "THONG CAO": "THÔNG CÁO",
    "THONG BAO": "THÔNG BÁO",
    "HUONG DAN": "HƯỚNG DẪN",
    "CHUONG TRINH": "CHƯƠNG TRÌNH",
    "KE HOACH": "KẾ HOẠCH",
    "PHUONG AN": "PHƯƠNG ÁN",
    "DE AN": "ĐỀ ÁN",
    "DU AN": "DỰ ÁN",
    "BAO CAO": "BÁO CÁO",
    "BIEN BAN": "BIÊN BẢN",
    "TO TRINH": "TỜ TRÌNH",
    "HOP DONG": "HỢP ĐỒNG",
    "CONG VAN": "CÔNG VĂN",
    "CONG DIEN": "CÔNG ĐIỆN",
    "BAN GHI NHO": "BẢN GHI NHỚ",
    "BAN THOA THUAN": "BẢN THỎA THUẬN",
    "GIAY UY QUYEN": "GIẤY ỦY QUYỀN",
    "GIAY MOI": "GIẤY MỜI",
    "GIAY GIOI THIEU": "GIẤY GIỚI THIỆU",
    "GIAY NGHI PHEP": "GIẤY NGHỈ PHÉP",
    "PHIEU GUI": "PHIẾU GỬI",
    "PHIEU CHUYEN": "PHIẾU CHUYỂN",
    "PHIEU BAO": "PHIẾU BÁO",
    "THU CONG": "THƯ CÔNG"
}


def strip_accents(text: str) -> str:
    """Loại bỏ dấu tiếng Việt để so khớp đối soát (phục vụ OCR/PDF bị lỗi bảng mã)"""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def get_standard_output_path(input_path: str, ext: str = ".docx") -> str:
    """Tự động sinh đường dẫn bản sao chuẩn hóa: [tên_gốc]_chuan_ND30.docx"""
    base, _ = os.path.splitext(input_path)
    return f"{base}{OUTPUT_SUFFIX}{ext}"


def sanitize_dashes(text: str) -> str:
    """
    Chuẩn hóa các loại dấu gạch ngang dài (Em-dash —, En-dash –) do AI sinh về dấu gạch nối ngắn (-)
    theo đúng quy chuẩn của Nghị định 30/2020/NĐ-CP:
    - Tiêu ngữ: 'Độc lập - Tự do - Hạnh phúc' (có dấu cách 2 bên)
    - Số ký hiệu: '123/QĐ-UBND' (viết liền không dấu cách)
    - Dấu gạch đầu dòng liệt kê: '- ' (dấu nối ngắn kèm khoảng trắng)
    - Giữa các từ/khoảng thời gian: ' - ' (có khoảng trắng 2 bên)
    """
    if not text:
        return ""

    # Bỏ qua nếu toàn bộ chuỗi là đường kẻ trang trí (ví dụ: '───────', '—————', '------')
    stripped = text.strip()
    if stripped and len(stripped) >= 3 and all(c in "—–─-_ " for c in stripped):
        return text

    # 1. Tiêu ngữ "Độc lập - Tự do - Hạnh phúc"
    text = re.sub(
        r"Độc\s*lập\s*[—–-]\s*Tự\s*do\s*[—–-]\s*Hạnh\s*phúc",
        "Độc lập - Tự do - Hạnh phúc",
        text,
        flags=re.IGNORECASE
    )

    # 2. Số và ký hiệu văn bản (chuyển — và – giữa các chữ viết tắt thành - không cách)
    # Ví dụ: 12/QĐ—UBND -> 12/QĐ-UBND
    text = re.sub(r"([A-ZĐ0-9]+)\s*[—–]\s*([A-ZĐ0-9]+)", r"\1-\2", text)

    # 3. Gạch ngang kèm khoảng trắng giữa câu: ' — ' hoặc ' – ' -> ' - '
    text = re.sub(r"\s+[—–]\s+", " - ", text)

    # 4. Gạch đầu dòng ở đầu câu/đoạn: '— ' hoặc '– ' -> '- '
    text = re.sub(r"^(\s*)[—–]\s*", r"\1- ", text)

    # 5. Các dấu — hoặc – đơn lẻ còn sót lại trong từ ngữ
    text = text.replace("—", "-").replace("–", "-")

    return text
