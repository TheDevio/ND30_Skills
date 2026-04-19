# Hướng dẫn Sử dụng Bộ hỗ trợ soạn thảo Văn bản Hành chính chuẩn Nghị định 30/2020/NĐ-CP

---

## Bộ Skills là gì?

Bộ Skills là **tập hợp các file hướng dẫn** được lưu trong thư mục `.agent/skills/` của dự án. Khi bạn chat với tôi (Antigravity) trong workspace này, tôi sẽ **tự động nhận diện** và đọc bộ skills để áp dụng đúng quy tắc Nghị định 30.

Nói cách khác: bộ skills là **"bộ nhớ chuyên môn"** mà tôi luôn mang theo khi làm việc với bạn trong thư mục này.

---

## Cấu trúc thư mục

```text
ND30_Skills/
├── .agent/
│   └── skills/
│       └── decree-30-formatting/
│           ├── 01-thong-so-ky-thuat.md    # Thông số lề, font, cỡ chữ
│           ├── 02-bang-mau-chu.md         # Mẫu chữ chi tiết
│           ├── 03-so-do-bo-cuc.md         # Sơ đồ bố cục trang
│           ├── 04-quy-tac-viet-hoa.md     # Quy tắc viết hoa
│           ├── 05-mau-van-ban.md          # Thư viện mẫu văn bản
│           ├── 06-ban-sao.md              # Quy định về bản sao
│           ├── 07-checklist.md            # Checklist kiểm tra
│           ├── SKILL.md                   # Định nghĩa Skill chính
│           └── scripts/
│               └── validate_docx.py       # Script kiểm tra tự động
├── huong_dan_su_dung_skills.md            # Hướng dẫn chi tiết
└── README.md                              # Tài liệu dự án
```

---

## Nhờ tôi (Antigravity) — Dùng ngôn ngữ tự nhiên

Đây là cách **đơn giản nhất**. Bạn chỉ cần mô tả việc cần làm, tôi sẽ tự đọc skill và thực hiện.

### Tình huống 1: Định dạng lại văn bản có sẵn

Bạn có file `.docx` cần chỉnh theo NĐ 30. Hãy nói:

> **Bạn:** "Định dạng lại file `Quyet_dinh_01.docx` theo Nghị định 30"

Tôi sẽ tự động:

1. Đọc `SKILL.md` → biết phải áp dụng quy trình gì
2. Đọc `01-thong-so-ky-thuat.md` → chỉnh lề, font, cỡ chữ
3. Đọc `02-bang-mau-chu.md` → chỉnh kiểu chữ từng thành phần
4. Đọc `03-so-do-bo-cuc.md` → sắp xếp bố cục đúng vị trí
5. Đọc `04-quy-tac-viet-hoa.md` → kiểm tra viết hoa
6. Dùng `python-docx` để sửa file
7. Chạy `validate_docx.py` để kiểm tra lần cuối

---

### Tình huống 2: Soạn mới một văn bản

Bạn cần tạo văn bản mới từ đầu. Hãy nói:

> **Bạn:** "Soạn một Quyết định về việc bổ nhiệm ông Nguyễn Văn A làm Trưởng phòng HC-TC, do Giám đốc Sở Nội vụ tỉnh Đồng Nai ký"

Tôi sẽ tự động:

1. Đọc `05-mau-van-ban.md` → lấy mẫu Quyết định (1.2 hoặc 1.4)
2. Điền thông tin bạn cung cấp vào mẫu
3. Áp dụng đúng font, cỡ chữ, bố cục từ bộ skills
4. Tạo file `.docx` hoàn chỉnh

---

### Tình huống 3: Kiểm tra văn bản

Bạn muốn biết file đã đúng chuẩn chưa. Hãy nói:

> **Bạn:** "Kiểm tra file `Cong_van_05.docx` có đúng Nghị định 30 không?"

Tôi sẽ tự động:

1. Chạy `validate_docx.py` để kiểm tra kỹ thuật
2. Đọc `07-checklist.md` → kiểm tra thủ công các mục không tự động hóa được
3. Báo cáo chi tiết: mục nào đạt, mục nào lỗi, cách sửa

---

### Tình huống 4: Hỏi quy tắc cụ thể

> **Bạn:** "Tên cơ quan UBND tỉnh Đồng Nai viết hoa thế nào?"

Tôi sẽ:

1. Đọc `04-quy-tac-viet-hoa.md`
2. Trả lời: **Ủ**y ban **n**hân dân tỉnh **Đ**ồng **N**ai

---

## Bảng tóm tắt: Khi nào dùng cách nào?

| Tình huống            | Cách tốt nhất            | Lý do                              |
| --------------------- | ------------------------ | ---------------------------------- |
| Soạn VB mới từ đầu    | **Nhờ tôi**              | Tôi tạo file .docx hoàn chỉnh luôn |
| Chỉnh lại VB có sẵn   | **Nhờ tôi**              | Tôi sửa trực tiếp file .docx       |
| Kiểm tra nhanh 1 file | **Script Python**        | Nhanh, tự động, chính xác          |
| Tra cứu quy tắc       | **Đọc file .md**         | Tự tra, không cần chờ              |
| In checklist kiểm tra | **Mở `07-checklist.md`** | In ra giấy, check từng mục         |

---

## Mẹo sử dụng hiệu quả

> [!TIP]
> **Mẹo 1:** Khi nhờ tôi, hãy đính kèm file bằng `@[đường dẫn file]` để tôi đọc trực tiếp.
>
> **Mẹo 2:** Copy mẫu từ `05-mau-van-ban.md` vào Word để soạn nhanh.
