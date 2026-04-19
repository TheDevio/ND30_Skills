---
name: decree-30-formatting
description: Bộ kỹ năng soạn thảo và định dạng văn bản hành chính theo Nghị định 30/2020/NĐ-CP. Bao gồm quy tắc trình bày, mẫu chữ, mẫu văn bản, quy tắc viết hoa, và checklist kiểm tra.
---

# 📜 Soạn thảo Văn bản Hành chính theo Nghị định 30/2020/NĐ-CP

## Mục đích
Skill này cung cấp **bộ quy tắc đầy đủ** để soạn thảo, định dạng và kiểm tra văn bản hành chính tuân thủ **Nghị định 30/2020/NĐ-CP** (ban hành ngày 05/03/2020).

## Khi nào sử dụng Skill này?
- Soạn mới văn bản hành chính (Quyết định, Công văn, Thông báo, Tờ trình, v.v.)
- Rà soát, chỉnh sửa định dạng văn bản hiện có cho đúng chuẩn
- Kiểm tra lỗi thể thức trình bày
- Tạo mẫu (template) văn bản cho cơ quan/tổ chức

## Cấu trúc bộ Skill

| File | Nội dung |
|------|----------|
| `SKILL.md` | File hướng dẫn chính (file này) |
| `01-thong-so-ky-thuat.md` | Thông số kỹ thuật: khổ giấy, lề, font, cỡ chữ |
| `02-bang-mau-chu.md` | Bảng mẫu chữ chi tiết cho từng thành phần văn bản |
| `03-so-do-bo-cuc.md` | Sơ đồ bố cục trang văn bản và vị trí các thành phần |
| `04-quy-tac-viet-hoa.md` | Quy tắc viết hoa trong văn bản hành chính |
| `05-mau-van-ban.md` | Mẫu các loại văn bản (Quyết định, Công văn, Thông báo...) |
| `06-ban-sao.md` | Quy định về bản sao văn bản |
| `07-checklist.md` | Checklist kiểm tra trước khi ban hành |
| `scripts/validate_docx.py` | Script Python kiểm tra định dạng file .docx |

## Quy trình làm việc

### Bước 1: Xác định loại văn bản
Xem file `05-mau-van-ban.md` để chọn đúng mẫu.

### Bước 2: Thiết lập trang
Áp dụng thông số từ `01-thong-so-ky-thuat.md` (lề, font, cỡ chữ).

### Bước 3: Soạn nội dung
Theo đúng bố cục trong `03-so-do-bo-cuc.md` và mẫu chữ trong `02-bang-mau-chu.md`.

### Bước 4: Kiểm tra viết hoa
Đối chiếu với `04-quy-tac-viet-hoa.md`.

### Bước 5: Rà soát cuối cùng
Sử dụng `07-checklist.md` và chạy script `scripts/validate_docx.py` (nếu dùng file .docx).
