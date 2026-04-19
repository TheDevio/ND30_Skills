# 📐 Thông số Kỹ thuật Trình bày Văn bản

> Theo Phụ lục I, Nghị định 30/2020/NĐ-CP

---

## 1. Khổ giấy & Hướng giấy

| Thông số | Giá trị |
|----------|---------|
| Khổ giấy | **A4** (210 mm × 297 mm) |
| Hướng giấy mặc định | **Dọc** (Portrait) |
| Hướng giấy ngoại lệ | Ngang (Landscape) — chỉ dùng cho bảng biểu, sơ đồ lớn |

---

## 2. Lề trang (Page Margins)

| Lề | Kích thước (mm) | Ghi chú |
|----|-----------------|---------|
| **Lề trên** (Top) | 20 – 25 mm | Thường dùng **20 mm** |
| **Lề dưới** (Bottom) | 20 – 25 mm | Thường dùng **20 mm** |
| **Lề trái** (Left) | 30 – 35 mm | Thường dùng **30 mm** (để đóng gáy) |
| **Lề phải** (Right) | 15 – 20 mm | Thường dùng **20 mm** |

> **Quy ước phổ biến**: Top 20, Bottom 20, Left 30, Right 20 (đơn vị mm).

### Cài đặt trong Word:
```
File → Page Setup → Margins:
  Top:    2.0 cm
  Bottom: 2.0 cm
  Left:   3.0 cm
  Right:  2.0 cm
```

### Cài đặt trong python-docx:
```python
from docx.shared import Mm

section = document.sections[0]
section.top_margin = Mm(20)
section.bottom_margin = Mm(20)
section.left_margin = Mm(30)
section.right_margin = Mm(20)
section.page_width = Mm(210)
section.page_height = Mm(297)
```

---

## 3. Phông chữ (Font)

| Thông số | Giá trị |
|----------|---------|
| **Phông chữ** | **Times New Roman** |
| **Bảng mã** | Unicode |
| **Tiêu chuẩn** | TCVN 6909:2001 |
| **Màu chữ** | Đen (Black) |

> ⚠️ **KHÔNG** dùng font khác (Arial, Calibri, v.v.) cho văn bản hành chính.

---

## 4. Cỡ chữ (Font Size)

| Thành phần | Cỡ chữ |
|-----------|---------|
| Quốc hiệu | 12 – 13 |
| Tiêu ngữ | 13 – 14 |
| Tên cơ quan chủ quản | 12 – 13 |
| Tên cơ quan ban hành | 12 – 13 |
| Số, ký hiệu | 13 |
| Địa danh, thời gian | 13 – 14 |
| Tên loại văn bản | 13 – 14 |
| Trích yếu nội dung | 13 – 14 |
| Nội dung văn bản | **13 – 14** |
| Chức vụ người ký | 13 – 14 |
| Họ tên người ký | 13 – 14 |
| Nơi nhận (tiêu đề) | 12 |
| Nơi nhận (danh sách) | 11 |
| Số trang | 13 – 14 |

### Quy tắc thống nhất cỡ chữ:
> Trong cùng một văn bản, các cỡ chữ phải **tăng/giảm đồng bộ**:
> - **Phương án 1**: Quốc hiệu 12 → Tiêu ngữ 13 → Nội dung 13
> - **Phương án 2**: Quốc hiệu 13 → Tiêu ngữ 14 → Nội dung 14

---

## 5. Khoảng cách dòng (Line Spacing)

| Thông số | Giá trị |
|----------|---------|
| Khoảng cách dòng | **Đơn (1.0)** hoặc **1.15 – 1.5** |
| Khoảng cách trước đoạn (Before) | **0 pt** (mặc định) hoặc **6 pt** |
| Khoảng cách sau đoạn (After) | **0 pt** (mặc định) hoặc **6 pt** |

### Cài đặt trong Word:
```
Format → Paragraph:
  Line spacing: Single hoặc 1.15
  Before: 0 pt
  After:  0 pt
```

---

## 6. Thụt đầu dòng & Căn lề

| Thông số | Giá trị |
|----------|---------|
| **Thụt đầu dòng** (First Line Indent) | **1.27 cm** (= 0.5 inch) |
| **Căn lề nội dung** | **Đều hai bên** (Justified) |
| **Căn lề tiêu đề** | **Giữa** (Center) |

---

## 7. Đánh số trang

| Thông số | Giá trị |
|----------|---------|
| Vị trí | **Giữa trang, phía trên** (Top Center) |
| Kiểu số | Số Ả Rập (1, 2, 3...) |
| Cỡ chữ | 13 – 14 |
| Trang đầu | Không đánh số trang 1 (bắt đầu từ trang 2) |

### Cài đặt trong Word:
```
Insert → Page Numbers:
  Position: Top of page
  Alignment: Center
  ☐ Show number on first page (bỏ chọn)
```

---

## 8. Dấu phân cách

| Thành phần | Dòng kẻ |
|-----------|---------|
| Dưới Quốc hiệu + Tiêu ngữ | Dòng kẻ ngang liền, **dài bằng phần chữ** |
| Dưới tên cơ quan ban hành | Dòng kẻ ngang liền, ngắn hơn |
| Dưới trích yếu nội dung | Dòng kẻ ngang liền, căn giữa |

> Dòng kẻ dùng ký tự gạch dưới hoặc border bottom, **không** dùng hình ảnh.

---

## 9. Tóm tắt nhanh — Copy & Paste

```
╔════════════════════════════════════════╗
║  THÔNG SỐ NHANH - NGHỊ ĐỊNH 30       ║
╠════════════════════════════════════════╣
║  Giấy:    A4, dọc                     ║
║  Font:    Times New Roman, đen         ║
║  Cỡ chữ: 13-14 (nội dung)            ║
║  Lề:     T20 - D20 - Tr30 - Ph20 mm  ║
║  Dòng:   1.0 hoặc 1.15               ║
║  Thụt:   1.27 cm                      ║
║  Căn lề: Justified (đều hai bên)      ║
║  Số trang: Giữa, trên, từ trang 2    ║
╚════════════════════════════════════════╝
```
