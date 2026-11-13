# ND30_Skills

**Bộ kỹ năng chuyên sâu soạn thảo, dựng khuôn và thẩm định thể thức văn bản hành chính theo Nghị định 30/2020/NĐ-CP.**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-2.2.0-blue.svg)
![Validator](https://img.shields.io/badge/Validator-ND30__Skills-success.svg)
![Safety](https://img.shields.io/badge/Non--Destructive-Original%20Safe-brightgreen.svg)
![Author](https://img.shields.io/badge/Author-The%20Devio-orange.svg)

---

| 🎯 **Mục tiêu hệ thống**                                 | 🛡️ **An toàn dữ liệu**                                            |
| :------------------------------------------------------- | :---------------------------------------------------------------- |
| Chuẩn hóa 100% thể thức theo **Nghị định 30/2020/NĐ-CP** | Bảo toàn tuyệt đối file gốc, luôn xuất bản sao `_chuan_ND30.docx` |

**ND30_Skills** là bộ kỹ năng chuyên sâu (Agent Skill) dành cho Trợ lý AI (như Antigravity) giúp tự động hóa toàn diện quy trình: **soạn mới**, **chuẩn hóa văn bản có sẵn**, **số hóa từ PDF scan/ký số** và **thẩm định thể thức** văn bản hành chính Việt Nam đạt độ chuẩn xác tuyệt đối theo quy định pháp luật hiện hành.

---

## 🛡️ 6 Nguyên tắc cốt lõi

1. **Bảo toàn file gốc tuyệt đối (Tiên quyết):** Khi người dùng cung cấp file `.docx` hoặc `.pdf` cần xử lý, hệ thống **tuyệt đối không ghi đè hoặc chỉnh sửa trực tiếp lên file gốc**. Mọi kết quả luôn được xuất ra một **bản sao mới** có tên chuẩn hóa: `[tên_gốc]_chuan_ND30.docx`.
2. **Thể thức do mã, không do model:** Bố cục bảng 2 cột ẩn viền (Quốc hiệu/Cơ quan, Nơi nhận/Chữ ký), lề trang A4 chuẩn, độ dài đường kẻ tiêu ngữ, căn đều hai bên và khoảng cách đoạn được tạo dựng chuẩn xác bằng mã Python (`builder_docx.py`), loại bỏ hoàn toàn việc AI ước lượng cảm tính gây méo vỡ khung.
3. **Chốt chặn chất lượng (Self-Healing Loop):** Sau khi tạo hoặc sửa file, hệ thống tự động kích hoạt bộ thẩm định thể thức chuyên sâu (`validate_docx.py`). Nếu còn lỗi thể thức, mã sẽ tự động hiệu chỉnh và thẩm định lại; **không bàn giao văn bản khi chưa đạt 100% chuẩn thể thức**.
4. **Không suy diễn (Zero Hallucination):** Số hiệu văn bản, ngày ban hành, tên người ký nếu chưa có dữ liệu sẽ được giữ nguyên dưới dạng placeholder chuẩn hóa `[...]` (ví dụ: `Số: [...]/QĐ-...`, `ngày [...] tháng [...] năm 20[...]`, người ký `[...]`). Hệ thống liệt kê chi tiết các vị trí cần hoàn thiện khi bàn giao.
5. **Hỏi gom một lần (Batch Clarification):** Nhận diện nhanh toàn bộ các trường thông tin còn thiếu và hỏi tập trung một lần duy nhất, tránh hỏi ngắt quãng nhiều lượt làm gián đoạn công việc của người dùng.
6. **Chuẩn hóa dấu gạch nối ngắn (ASCII 45):** Khắc phục triệt để lỗi đặc trưng của các mô hình AI khi tự ý dùng dấu gạch ngang dài `—` (Em-dash) hoặc `–` (En-dash). Hệ thống bắt buộc chỉ sử dụng dấu gạch nối ngắn `-` (phím `-`, ASCII 45) cho Tiêu ngữ (`Độc lập - Tự do - Hạnh phúc`), Số ký hiệu (`/QĐ-UBND`) và gạch đầu dòng (`- `). Bộ validator tự động bắt lỗi và builder tự động thanh lọc về `-`.

---

## 🚀 Tính năng nổi bật

- **Bộ dựng văn bản bằng mã (`builder_docx.py`):** Dựng khung Word chuẩn với bảng 2 ô ẩn viền, đường kẻ nét liền tỷ lệ chuẩn (100% dòng Tiêu ngữ, 1/3-1/2 dòng Cơ quan), số trang ở giữa lề trên và định dạng phông Times New Roman chuẩn Unicode TCVN 6909:2001.
- **Bộ thẩm định thể thức tự động (`validate_docx.py`):** Quét sâu cấu trúc file Word (paragraphs, tables, runs, header/footer và XML lõi), tự động phát hiện 40+ lỗi thể thức và hỗ trợ xuất báo cáo JSON.
- **Bộ số hóa văn bản từ PDF (`pdf_to_docx.py`):** Bóc tách ngữ nghĩa từ file PDF scan hoặc ký số và tái sinh thành bản thảo Word sạch 100%, không sử dụng text-box chắp vá hay làm vỡ layout.
- **Giao diện trực quan hóa toàn diện (by The Devio):**
  - [**project_architecture.html**](project_architecture.html): Bản đồ kiến trúc hệ thống và mô phỏng trang A4 tương tác liên kết bảng thông số kỹ thuật.
  - [**skills_workflow.html**](skills_workflow.html): Sơ đồ luồng hoạt động 6 bước khép kín, cơ chế tự sửa lỗi (Self-Healing Loop) và trình mô phỏng thực thi trực quan.
- **Hệ thống mẫu biểu & Quy chuẩn toàn diện:** Bảng viết tắt 29 loại văn bản hành chính (Quy định là `QyĐ`), hệ thống 15 mẫu chính thức (Mẫu 1.1-1.10, Phụ lục 2.1-2.2, Bản sao 3.1-3.2), cẩm nang quy tắc viết hoa (Phụ lục II), nghiệp vụ quản lý văn bản đi/đến (8 mẫu sổ Phụ lục IV), lập hồ sơ nộp lưu (Phụ lục V) và chuẩn siêu dữ liệu (Metadata) điện tử (Phụ lục VI).

---

## 📂 Cấu trúc thư mục dự án

```text
ND30_Skills_v2/
├── .agent/
│   └── skills/
│       └── ND30_Skills/                   # Bộ kỹ năng tích hợp cho Trợ lý AI (Antigravity)
│           ├── 01-thong-so-ky-thuat.md    # Khổ giấy, lề trang, font, dải cỡ chữ, chuẩn ký số (Phụ lục I)
│           ├── 02-bang-mau-chu.md         # Quy chuẩn kiểu chữ 14 thành phần thể thức theo Mục V Phụ lục I
│           ├── 03-so-do-bo-cuc.md         # Sơ đồ 14 ô vị trí thể thức & 7 ô khối bản sao giấy (Mục IV Phụ lục I)
│           ├── 04-quy-tac-viet-hoa.md     # Quy tắc viết hoa tên cơ quan, chức vụ, địa danh, điều khoản (Phụ lục II)
│           ├── 05-mau-van-ban.md          # 29 chữ viết tắt (Quy định là QyĐ) & 15 mẫu chuẩn (Phụ lục III)
│           ├── 06-ban-sao.md              # Thể thức bản sao giấy (7 thành phần) & bản sao điện tử (ô 14)
│           ├── 07-checklist.md            # Bảng kiểm tra 40+ tiêu chí rà soát trước khi ký ban hành
│           ├── 08-quan-ly-van-ban.md      # 8 Mẫu sổ văn thư, Bì thư, Dấu ĐẾN 35x50mm có Số/KH hồ sơ (Phụ lục IV)
│           ├── 09-lap-ho-so-luu-tru.md    # Nghiệp vụ lập hồ sơ, Danh mục hồ sơ, Mục lục nộp lưu 7 cột (Phụ lục V)
│           ├── 10-tai-lieu-dien-tu-metadata.md # Quản lý tài liệu điện tử & 3 bảng Metadata đặc tả (Phụ lục VI)
│           ├── SKILL.md                   # Hướng dẫn vận hành, quy trình 6 bước khép kín và 6 nguyên tắc cốt lõi
│           └── scripts/
│               ├── constants.py           # Hệ thống hằng số, quy chuẩn kỹ thuật, regex kiểm tra
│               ├── builder_docx.py        # Module dựng file Word chuẩn thể thức bằng mã Python thuần túy
│               ├── pdf_to_docx.py         # Module số hóa văn bản từ PDF sang Word sạch
│               └── validate_docx.py       # Bộ thẩm định thể thức văn bản chuyên sâu quét cấu trúc XML/DOM
├── 30.signed.pdf                          # Văn bản gốc Nghị định 30/2020/NĐ-CP ký số từ Cổng TTĐT Chính phủ
├── project_architecture.html              # Giao diện trực quan kiến trúc & blueprint A4 tương tác (by The Devio)
├── skills_workflow.html                   # Giao diện trực quan luồng hoạt động & simulator tương tác (by The Devio)
├── LICENSE                                # Giấy phép mã nguồn mở MIT
└── README.md                              # Tài liệu dự án (by The Devio)
```

---

## 🔄 Quy trình 6 bước chuẩn hóa

```text
[Bước 1] Nhận diện loại văn bản (Quyết định Mẫu 1.2/1.3, Công văn Mẫu 1.5, Tờ trình Mẫu 1.6...)
   ↓
[Bước 2] Thu thập thông tin (Hỏi gom 1 lần duy nhất; áp dụng Zero Hallucination [...])
   ↓
[Bước 3] Dựng file Word bằng mã (builder_docx.py: lề chuẩn, font TNR, bảng 2 cột ẩn viền, gạch '-')
   ↓
[Bước 4] Tự thẩm định thể thức (validate_docx.py quét 40+ tiêu chí; Self-Healing Loop tự sửa nếu lỗi)
   ↓
[Bước 5] Bàn giao file đạt chuẩn 100% PASS & Liệt kê danh sách vị trí để trống [...] cần hoàn thiện
   -----------
[Bước 6] Xử lý file có sẵn (BẢO VỆ FILE GỐC: tạo bản sao [tên]_chuan_ND30.docx và thẩm định lại)
```

---

## 💬 Hướng dẫn sử dụng

### 1. Tương tác cùng Trợ lý AI (Antigravity hoặc AI hỗ trợ Skills)

Khi mở dự án trong môi trường hỗ trợ Agent Skills, trợ lý AI sẽ tự động kích hoạt bộ skill `ND30_Skills`. Người dùng chỉ cần đưa ra yêu cầu bằng ngôn ngữ tự nhiên:

- **Định dạng lại file văn bản có sẵn:**

  > _"Định dạng lại file `@[Bao_cao_01.docx]` theo Nghị định 30"_
  > $\rightarrow$ AI bảo toàn file gốc, tạo bản sao `Bao_cao_01_chuan_ND30.docx`, quét thẩm định và bàn giao kèm báo cáo chi tiết.

- **Số hóa văn bản từ file PDF:**

  > _"Số hóa file `@[Quyet_dinh_05.pdf]` sang Word chuẩn Nghị định 30 giúp tôi"_
  > $\rightarrow$ AI bóc tách nội dung, dựng file Word mới sạch 100%, tự chạy bộ kiểm định và trả về file Word đạt chuẩn.

- **Soạn mới văn bản hành chính:**

  > _"Soạn một Quyết định về việc phân công công tác cho cán bộ, do Giám đốc Sở Thông tin và Truyền thông Thành phố Hồ Chí Minh ký"_
  > $\rightarrow$ AI tải mẫu chuẩn, dựng file bằng mã, tự thẩm định và gửi file kèm danh mục các trường để trống dạng `[...]` cần điền bổ sung.

- **Thẩm định thể thức file văn bản:**

  > \_"Kiểm tra file `@[Cong_van_05.docx]` có đúng thể thức Nghị định 30 không?"\*
  > $\rightarrow$ AI quét toàn bộ các chỉ số thể thức và trả về bảng báo cáo: Đạt, Cảnh báo, Lỗi cần sửa.

- **Tra cứu quy tắc thể thức:**

  > \_"Tên cơ quan 'Sở Thông tin và Truyền thông Thành phố Hồ Chí Minh' viết hoa thế nào?"\*
  > $\rightarrow$ AI trả lời chính xác theo quy chuẩn: **S**ở **T**hông tin và **T**ruyền thông **T**hành phố **H**ồ **C**hí **M**inh (tra cứu từ `04-quy-tac-viet-hoa.md`).

---

### 2. Thực thi trực tiếp qua dòng lệnh (CLI)

Người dùng có thể chạy độc lập các công cụ kiểm định và tạo văn bản qua console:

```powershell
# Cài đặt thư viện phụ thuộc:
pip install python-docx PyMuPDF

# 1. Thẩm định thể thức văn bản Word:
python .agent/skills/ND30_Skills/scripts/validate_docx.py "duong_dan_file.docx"

# 2. Xuất kết quả thẩm định dưới dạng JSON:
python .agent/skills/ND30_Skills/scripts/validate_docx.py "duong_dan_file.docx" --json

# 3. Chuẩn hóa file (bảo toàn file gốc, tạo bản sao _chuan_ND30.docx):
python .agent/skills/ND30_Skills/scripts/builder_docx.py --format "Bao_cao_01.docx"

# 4. Số hóa file PDF sang Word chuẩn Nghị định 30:
python .agent/skills/ND30_Skills/scripts/pdf_to_docx.py "Quyet_dinh_goc.pdf"

# 5. Tạo nhanh file Quyết định mẫu:
python .agent/skills/ND30_Skills/scripts/builder_docx.py "Quyet_dinh_moi.docx"
```

---

## 📋 Danh mục tiêu chuẩn thẩm định thể thức

| Hạng mục kiểm tra           | Tiêu chuẩn quy định theo Nghị định 30/2020/NĐ-CP                                                                                                                          |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Thiết lập trang**         | Khổ giấy A4 (210×297 mm), hướng dọc; lề trên 20-25mm, lề dưới 20-25mm, lề trái 30-35mm, lề phải 15-20mm                                                                   |
| **Phông & Cỡ chữ**          | 100% phông chữ Times New Roman bộ mã Unicode TCVN 6909:2001; dải cỡ chữ chuẩn quy định (11, 12, 13, 14pt)                                                                 |
| **Dấu gạch nối ngắn**       | Chỉ dùng phím gạch nối ngắn `-` (ASCII 45) cho Tiêu ngữ, Số ký hiệu, gạch đầu dòng. Triệt tiêu hoàn toàn Em-dash `—` và En-dash `–`                                       |
| **Đầu trang & Quốc hiệu**   | Bảng 2 ô ẩn viền; Quốc hiệu & Tiêu ngữ chuẩn kiểu chữ; đường kẻ tiêu ngữ bằng 100% dòng chữ; tên cơ quan ban hành kèm đường kẻ 1/3-1/2 dòng chữ; Số ký hiệu đúng quy cách |
| **Quy tắc số 0 Ngày/Tháng** | Ngày nhỏ hơn 10 và tháng 1, 2 bắt buộc ghi thêm số 0 (`ngày 05`, `tháng 01`); từ tháng 3 đến tháng 12 không ghi số 0 (`tháng 3`, `tháng 12`)                              |
| **Thẩm quyền người ký**     | Đúng 5 trường hợp viết tắt: `TM.`, `Q.`, `KT.`, `TL.`, `TUQ.`. Tuyệt đối không ghi học hàm, học vị (GS., TS., ThS.)                                                       |
| **Nội dung văn bản**        | Căn đều hai bên (Justify); Thụt lề đầu dòng 1-1.27cm; Giãn dòng 1.0-1.15; Dấu kết thúc văn bản (`./.` hoặc `./`)                                                          |
| **Chân trang & Nơi nhận**   | Bảng 2 ô ẩn viền; Mục "Nơi nhận:" (đậm nghiêng 12pt, danh sách 11pt đứng gạch đầu dòng `- `); Chức vụ & Họ tên người ký                                                   |

---

## 💡 Khuyến nghị & Mẹo hay

> [!NOTE]
> **Đính kèm file thuận tiện:** Kẹp file trực tiếp vào câu hỏi bằng cú pháp `@[tên_file.docx]` hoặc `@[tên_file.pdf]` để AI tự động thẩm định và xử lý. File gốc luôn được bảo toàn tuyệt đối.

> [!TIP]
> **Rà soát in ấn:** Sử dụng bảng danh mục kiểm tra trong tài liệu `07-checklist.md` khi cần in ra giấy để rà soát văn bản trước khi trình lãnh đạo ký duyệt.

> [!IMPORTANT]
> **Khám phá giao diện trực quan:** Mở [skills_workflow.html](skills_workflow.html) hoặc [project_architecture.html](project_architecture.html) trên trình duyệt để trải nghiệm bản đồ kiến trúc, cây quyết định và mô phỏng trực quan trang A4 chuẩn thể thức.

---

## 🎁 Bản quyền & Ủng hộ

Dự án này là **HOÀN TOÀN MIỄN PHÍ VÀ MÃ NGUỒN MỞ (MIT)** dành cho cán bộ, công chức, viên chức và tất cả những ai làm công tác văn phòng tại Việt Nam.

🌟 **Nếu bạn thấy dự án hữu ích, hãy tặng 1 Star ⭐ trên GitHub nhé!** Đây là nguồn động viên quý giá để tiếp tục hoàn thiện và cập nhật thêm nhiều tiện ích mới.

---

## 🤝 Đóng góp

Mọi đóng góp (Pull Request), báo lỗi (Issue) hoặc gợi ý thêm mẫu văn bản mới đều được trân trọng. Hãy cùng nhau xây dựng môi trường làm việc hành chính chuẩn mực, hiện đại và hiệu quả!

---

_Phát triển bởi Dung "Devio" Le Quoc ❤️ - Vì mục tiêu hiện đại hóa và chuẩn hóa nền hành chính Việt Nam._
