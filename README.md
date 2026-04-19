# 📜 ND30\_-_Skills: Bộ hỗ trợ soạn thảo Văn bản Hành chính chuẩn Nghị định 30/2020/NĐ-CP

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)
![PRs-Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**ND30_Skills** là một bộ công cụ và quy tắc (Skills) được thiết kế đặc biệt để tích hợp vào các trợ lý AI mã nguồn mở (như Antigravity) hoặc sử dụng độc lập, giúp việc soạn thảo văn bản hành chính tại Việt Nam trở nên chuẩn xác, nhanh chóng và chuyên nghiệp theo đúng **Nghị định 30/2020/NĐ-CP**.

---

## ✨ Tính năng nổi bật

- ✅ **Chuẩn hóa:** Tuân thủ tuyệt đối các quy định về thể thức và kỹ thuật trình bày của Nghị định 30.
- 📋 **Thư viện mẫu đa dạng:** Cung cấp sẵn các mẫu Quyết định, Công văn, Tờ trình, Thông báo... chỉ việc điền nội dung.
- 📏 **Thông số kỹ thuật chi tiết:** Định nghĩa chính xác khổ giấy, lề, font chữ, cỡ chữ và kiểu chữ cho từng thành phần.
- 🔠 **Quy tắc viết hoa:** Hệ thống hóa các quy tắc viết hoa trong văn bản hành chính (tên cơ quan, chức vụ, địa danh...).
- ⚙️ **Kiểm tra tự động:** Script Python đi kèm giúp quét và phát hiện lỗi định dạng trong file `.docx` chỉ trong vài giây.
- 📝 **Checklist 40+ mục:** Bộ câu hỏi kiểm tra cuối cùng trước khi ký ban hành để đảm bảo không sai sót.

---

## 📂 Cấu trúc dự án

Bộ công cụ được tổ chức khoa học trong thư mục `.agent/skills/decree-30-formatting/`:

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

## 🚀 Cách sử dụng

### Dùng với Trợ lý AI (Khuyên dùng)

Nếu bạn đang sử dụng **Antigravity** hoặc các AI hỗ trợ Skills, bạn chỉ cần đưa ra yêu cầu:

- _"Định dạng lại file Báo cáo này theo Nghị định 30"_
- _"Soạn cho tôi một Quyết định khen thưởng đúng chuẩn"_

AI sẽ tự động đọc bộ quy tắc này để thực hiện chính xác cho bạn.

### Dùng thủ công

Bạn có thể mở trực tiếp các file `.md` trong thư mục `skills` để tra cứu nhanh quy tắc hoặc copy mẫu văn bản vào Word.

### Chạy Script kiểm tra

```powershell
pip install python-docx
python scripts/validate_docx.py "duong_dan_file_cua_ban.docx"
```

> [!TIP]
> Để hiểu rõ hơn về cách tận dụng tối đa bộ skills này, hãy xem [Hướng dẫn sử dụng chi tiết](huong_dan_su_dung_skills.md).

---

## 🎁 Bản quyền & Ủng hộ

Dự án này là **HOÀN TOÀN MIỄN PHÍ** dành cho cán bộ, công chức, viên chức và những người làm công tác văn phòng tại Việt Nam.

🌟 **Nếu mọi người thấy dự án hữu ích, hãy tặng mình 1 Star ⭐ trên GitHub nhé!** Đây là động lực lớn nhất để mình tiếp tục cập nhật và hoàn thiện bộ công cụ này.

---

## 🤝 Đóng góp

Mọi đóng góp (Pull Request), báo lỗi (Issue) hoặc gợi ý thêm mẫu văn bản mới đều được trân trọng. Hãy cùng nhau xây dựng một cộng đồng làm việc chuyên nghiệp hơn!

---

_Phát triển bởi TheDevio aka Quoc Dung Le ❤️ và vì mục tiêu hiện đại hóa nền hành chính Việt Nam._
