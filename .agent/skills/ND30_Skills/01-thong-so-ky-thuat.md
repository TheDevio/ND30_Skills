# 📐 Thông số Kỹ thuật Trình bày Văn bản Hành chính

> Căn cứ Phụ lục I, Nghị định 30/2020/NĐ-CP của Chính phủ

---

## 1. Khổ giấy & Hướng giấy

| Thông số | Giá trị chuẩn | Ghi chú |
|----------|---------------|---------|
| Khổ giấy | **A4** (210 mm x 297 mm) | Sai số cho phép +/- 2 mm |
| Hướng giấy mặc định | **Dọc** (Portrait) | Áp dụng cho toàn bộ văn bản thông thường |
| Hướng giấy ngoại lệ | **Ngang** (Landscape) | Chỉ dùng riêng cho bảng biểu, sơ đồ lớn kèm theo |

---

## 2. Lề trang (Page Margins)

| Lề | Kích thước (mm) | Giá trị mặc định khuyến nghị |
|----|-----------------|-----------------------------|
| **Lề trên** (Top) | 20 - 25 mm | **20 mm** |
| **Lề dưới** (Bottom) | 20 - 25 mm | **20 mm** |
| **Lề trái** (Left) | 30 - 35 mm | **30 mm** (dành cho đóng gáy tài liệu) |
| **Lề phải** (Right) | 15 - 20 mm | **20 mm** (hoặc 15 mm) |

> **Cài đặt chuẩn trong Word:**
> - Top: 2.0 cm | Bottom: 2.0 cm | Left: 3.0 cm | Right: 2.0 cm (hoặc 1.5 cm)

> **Cài đặt trong python-docx:**
> ```python
> from docx.shared import Mm
> section = document.sections[0]
> section.top_margin = Mm(20)
> section.bottom_margin = Mm(20)
> section.left_margin = Mm(30)
> section.right_margin = Mm(20)
> section.page_width = Mm(210)
> section.page_height = Mm(297)
> ```

---

## 3. Phông chữ (Font)

| Thông số | Giá trị bắt buộc |
|----------|------------------|
| **Phông chữ** | **Times New Roman** |
| **Bảng mã** | Unicode (TCVN 6909:2001) |
| **Màu chữ** | Đen (Black) |

> ⚠️ **Tuyệt đối KHÔNG** sử dụng các phông chữ khác như Arial, Calibri, Roboto... cho phần nội dung và thể thức văn bản hành chính nhà nước.

---

## 4. Dải Cỡ chữ (Font Size) Thống nhất

| STT | Thành phần thể thức | Cỡ chữ chuẩn | Kiểu chữ quy định |
|:---:|---------------------|:------------:|-------------------|
| 1 | Quốc hiệu | 12 - 13 | In hoa, đứng, đậm |
| 2 | Tiêu ngữ | 13 - 14 | In thường, đứng, đậm |
| 3 | Tên CQ chủ quản (cấp trên) | 12 - 13 | In hoa, đứng, thường |
| 4 | Tên CQ ban hành văn bản | 12 - 13 | In hoa, đứng, đậm |
| 5 | Số, ký hiệu văn bản | 13 | In thường, đứng, thường |
| 6 | Địa danh và thời gian ban hành | 13 - 14 | In thường, nghiêng |
| 7 | Tên loại văn bản | 13 - 14 | In hoa, đứng, đậm |
| 8 | Trích yếu nội dung văn bản có tên loại | 13 - 14 | In thường, đứng, đậm |
| 9 | Trích yếu nội dung Công văn (V/v) | 12 - 13 | In thường, đứng, thường |
| 10 | Nội dung văn bản | **13 - 14** | In thường, đứng, thường |
| 11 | Quyền hạn người ký (TM., Q., KT., TL., TUQ.) | 13 - 14 | In hoa, đứng, đậm |
| 12 | Chức vụ người ký | 13 - 14 | In hoa, đứng, đậm |
| 13 | Họ và tên người ký | 13 - 14 | In thường, đứng, đậm |
| 14 | Nơi nhận (từ "Nơi nhận:") | 12 | In thường, nghiêng, đậm |
| 15 | Nơi nhận (danh sách cơ quan nhận) | 11 | In thường, đứng, thường |
| 16 | Số trang văn bản | 13 - 14 | Số Ả Rập, đứng, thường |

### Quy tắc đồng bộ cỡ chữ:
Trong cùng một văn bản, cỡ chữ phải tăng/giảm **đồng bộ** theo 2 phương án:
- **Phương án 1 (cỡ nhỏ):** Quốc hiệu 12 -> Tiêu ngữ 13 -> Nội dung 13 -> Chữ ký 13.
- **Phương án 2 (cỡ lớn):** Quốc hiệu 13 -> Tiêu ngữ 14 -> Nội dung 14 -> Chữ ký 14.

---

## 5. Khoảng cách dòng & Khoảng cách đoạn

| Thông số | Giá trị quy định |
|----------|------------------|
| **Khoảng cách dòng (Line spacing)** | **Đơn (Single/1.0)** hoặc **1.15 - 1.5 dòng** |
| **Khoảng cách trước đoạn (Space before)** | **0 pt** hoặc tối thiểu **6 pt** giữa các phần |
| **Khoảng cách sau đoạn (Space after)** | **0 pt** hoặc tối thiểu **6 pt** |
| **Thụt đầu dòng đoạn văn (Indent)** | **1.0 - 1.27 cm** (mặc định chuẩn: 1.27 cm = 0.5 inch) |
| **Căn lề nội dung chính** | **Căn đều hai bên** (Justified) |

---

## 6. Đánh số trang Văn bản

| Thông số | Quy định chuẩn |
|----------|----------------|
| **Vị trí** | Chính giữa lề trên của trang (Header Center) |
| **Kiểu số** | Số Ả Rập (1, 2, 3...) |
| **Phông & cỡ chữ** | Times New Roman, cỡ **13 - 14**, đứng, thường |
| **Trang đầu tiên** | **Không đánh số trang 1** (bắt đầu hiển thị số `2` từ trang thứ hai) |
| **Ký tự kèm theo** | Không thêm từ "Trang", dấu gạch ngang `- 2 -` hay bất kỳ ký tự nào khác |

---

## 7. Quy tắc Độ dài Đường kẻ ngang Phân cách

Căn cứ Điểm b Khoản 1, Khoản 2 và Khoản 5 Mục II Phụ lục I:

| Vị trí đường kẻ | Tỷ lệ độ dài | Quy cách hiển thị |
|-----------------|--------------|-------------------|
| **Dưới dòng Tiêu ngữ** | **Bằng độ dài của dòng chữ** | Nét liền, đặt cân đối ngay dưới dòng chữ "Độc lập - Tự do - Hạnh phúc" |
| **Dưới Tên cơ quan ban hành** | **Bằng từ 1/3 đến 1/2 độ dài của dòng chữ** | Nét liền, đặt cân đối ngay dưới dòng tên cơ quan ban hành |
| **Dưới Trích yếu nội dung văn bản có tên loại** | **Bằng từ 1/3 đến 1/2 độ dài của dòng chữ** | Nét liền, đặt cân đối ngay dưới dòng trích yếu nội dung |

> ⚠️ Đường kẻ dùng thuộc tính Border Bottom hoặc ký tự nét liền `─`, tuyệt đối không chèn đối tượng Shape hoặc hình ảnh tự vẽ dễ bị xô lệch vị trí.

---

## 8. Quy tắc Ghi Số 0 tại Ngày, Tháng Ban hành Văn bản

> Căn cứ Điểm b Khoản 4 Mục II Phụ lục I:
> *"đối với những số thể hiện ngày nhỏ hơn 10 và tháng 1, 2 phải ghi thêm số 0 phía trước."*

| Thành phần | Quy tắc thể hiện | Ví dụ đúng (✅) | Ví dụ sai (❌) |
|------------|------------------|----------------|----------------|
| **Ngày < 10** | **Bắt buộc thêm số 0** phía trước | `ngày 05`, `ngày 09` | `ngày 5`, `ngày 9` |
| **Ngày >= 10** | Giữ nguyên 2 chữ số | `ngày 10`, `ngày 25` | `ngày 010` |
| **Tháng 1 và Tháng 2** | **Bắt buộc thêm số 0** phía trước | `tháng 01`, `tháng 02` | `tháng 1`, `tháng 2` |
| **Tháng 3 đến Tháng 12** | **KHÔNG thêm số 0** phía trước | `tháng 3`, `tháng 8`, `tháng 12` | `tháng 03`, `tháng 08` |

**Ví dụ ngày tháng hoàn chỉnh chuẩn Nghị định 30:**
- ✅ `Hà Nội, ngày 05 tháng 01 năm 2026`
- ✅ `Thành phố Hồ Chí Minh, ngày 09 tháng 02 năm 2026`
- ✅ `Đà Nẵng, ngày 15 tháng 3 năm 2026`
- ✅ `Hải Phòng, ngày 28 tháng 12 năm 2026`
- ❌ `Hà Nội, ngày 5 tháng 1 năm 2026` *(Sai: thiếu số 0 ở ngày 5 và tháng 1)*
- ❌ `Đà Nẵng, ngày 15 tháng 03 năm 2026` *(Sai: thừa số 0 ở tháng 3)*

---

## 9. Tiêu chuẩn Kỹ thuật Chữ ký số trong Văn bản Điện tử

> Căn cứ Khoản 7, Khoản 8 Mục II, Mục III Phần II Phụ lục I và Điều 12, 13 Nghị định 30/2020/NĐ-CP

| Thành phần ký số | Quy cách kỹ thuật | Vị trí hiển thị |
|------------------|-------------------|-----------------|
| **Chữ ký số của cá nhân (người có thẩm quyền)** | - Hình ảnh chữ ký tay trên giấy<br>- **Màu xanh** (Blue)<br>- Định dạng **PNG nền trong suốt** (Transparent) | Trình bày tại ô số 7b; căn giữa vào khoảng giữa chức vụ và họ tên người ký; **không trùm đè** lên họ và tên. |
| **Chữ ký số của cơ quan, tổ chức ban hành** | - Hình ảnh con dấu cơ quan, tổ chức<br>- **Màu đỏ** (Red), kích thước bằng kích thước thực tế con dấu<br>- Định dạng **PNG nền trong suốt**<br>- Kèm thông tin: Tên cơ quan, tổ chức và thời gian ký số (ngày, tháng, năm; giờ, phút, giây; múi giờ Việt Nam theo ISO 8601) | Trùm lên khoảng **1/3 chữ ký số của người có thẩm quyền về phía bên trái**. |
| **Chữ ký số trên Phụ lục / Văn bản kèm theo** | - **Không hiển thị hình ảnh con dấu**<br>- Thông tin hiển thị: Số và ký hiệu văn bản; thời gian ký (ngày, tháng, năm; giờ, phút, giây; múi giờ VN theo ISO 8601)<br>- Phông Times New Roman, in thường, đứng, **cỡ chữ 10**, màu đen | Trình bày tại **góc trên bên phải**, trang đầu của phụ lục hoặc văn bản kèm theo. |
| **Chữ ký số trên Bản sao điện tử** | - **Không hiển thị hình ảnh con dấu đỏ**<br>- Thông tin hiển thị: Hình thức sao; Tên cơ quan, tổ chức sao; thời gian ký<br>- Phông Times New Roman, in thường, đứng, **cỡ chữ 10**, màu đen | Trình bày tại **ô số 14** (góc trên bên phải, trang đầu của bản sao điện tử). |

---

## 10. Tóm tắt nhanh Thông số Kỹ thuật

```
+-------------------------------------------------------------------+
|  THÔNG SỐ KỸ THUẬT VĂN BẢN HÀNH CHÍNH - NGHỊ ĐỊNH 30/2020/NĐ-CP   |
+-------------------------------------------------------------------+
|  Khổ giấy:    A4 (210 mm x 297 mm), hướng dọc                     |
|  Font chữ:    Times New Roman, bảng mã Unicode (TCVN 6909:2001)   |
|  Cỡ chữ:      13 - 14 pt (nội dung chính)                         |
|  Lề trang:    Trên 20-25 | Dưới 20-25 | Trái 30-35 | Phải 15-20 mm|
|  Mặc định:    Top 20 - Bottom 20 - Left 30 - Right 20 mm          |
|  Giãn dòng:   Đơn (1.0) hoặc 1.15; Đoạn trước/sau: 0 - 6 pt       |
|  Thụt lề:     1.27 cm (First line indent)                         |
|  Căn lề:      Justified (đều hai bên)                             |
|  Số trang:    Giữa, lề trên (Header center), từ trang 2, 13-14 pt |
|  Đường kẻ:    Tiêu ngữ: 100% | Cơ quan & Trích yếu: 1/3 đến 1/2   |
|  Ngày tháng:  Ngày < 10 và Tháng 01, 02 có số 0; Tháng 3-12 không |
|  Ký số người: Màu xanh, PNG trong suốt, ô 7b                      |
|  Ký số CQ:    Dấu đỏ thật trùm 1/3 chữ ký bên trái + thời gian ký |
+-------------------------------------------------------------------+
```
