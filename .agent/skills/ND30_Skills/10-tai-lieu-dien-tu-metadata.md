# 💻 Hệ thống Quản lý Tài liệu Điện tử & Chuẩn Siêu Dữ liệu (Metadata)

> Căn cứ Chương II, Chương III và Phụ lục VI, Nghị định 30/2020/NĐ-CP của Chính phủ

---

## I. YÊU CẦU CHỨC NĂNG CỦA HỆ THỐNG QUẢN LÝ TÀI LIỆU ĐIỆN TỬ

Căn cứ Phần I, Phụ lục VI, Nghị định 30/2020/NĐ-CP chuẩn hóa các yêu cầu chức năng tối thiểu đối với Hệ thống quản lý tài liệu điện tử của cơ quan, tổ chức:

1. **Quản lý toàn bộ vòng đời văn bản:**
   - Quản lý tập trung từ khâu soạn thảo, lấy ý kiến, duyệt bản thảo, ký số, phát hành, tiếp nhận, chuyển giao xử lý, lập hồ sơ điện tử và nộp lưu hồ sơ vào Lưu trữ điện tử cơ quan.
2. **Ký số và Xác thực chữ ký số:**
   - Tích hợp dịch vụ chứng thực chữ ký số chuyên dùng Chính phủ hoặc chữ ký số công cộng hợp pháp theo quy định của pháp luật.
   - Tự động kiểm tra tính hợp lệ của chứng thư số, dấu thời gian và tính toàn vẹn của tệp dữ liệu văn bản điện tử.
3. **Kết nối liên thông văn bản:**
   - Tuân thủ Quy chuẩn kỹ thuật quốc gia về mã định danh và định dạng gói tin gửi nhận văn bản điện tử phục vụ kết nối thông suốt qua **Trục liên thông văn bản quốc gia**.
4. **Định dạng tệp văn bản chính thức:**
   - Văn bản điện tử phát hành chính thức phải ở định dạng **Portable Document Format (.pdf)** phiên bản 1.4 trở lên hoặc chuẩn **PDF/A** (chuẩn tài liệu lưu trữ dài hạn).
   - Văn bản số hóa quét từ văn bản giấy: định dạng PDF, độ phân giải tối thiểu 200 dpi, tỷ lệ quét 100%, màu hoặc đen trắng rõ nét.

---

## II. BẢNG I: DỮ LIỆU THÔNG TIN ĐẦU VÀO CỦA VĂN BẢN ĐI

> Căn cứ Bảng I, Phần II, Phụ lục VI (Trang 74 - 75 Nghị định 30/2020/NĐ-CP):

| STT | Tên trường tiếng Việt | Tên trường tiếng Anh | Kiểu dữ liệu | Mô tả theo Nghị định 30 |
|:---:|-----------------------|:--------------------:|:------------:|-------------------------|
| 1 | Mã hồ sơ | `FileCode` | Chuỗi ký tự | Mã hồ sơ theo Danh mục hồ sơ cơ quan |
| 2 | Mã định danh cơ quan, tổ chức | `OrganId` | Chuỗi ký tự | Mã định danh cơ quan ban hành văn bản |
| 3 | Năm mục lục hồ sơ | `FileCatalog` | Số nguyên | Năm lập hồ sơ (VD: `2026`) |
| 4 | Số và ký hiệu hồ sơ | `FileNotation` | Chuỗi ký tự | Ký hiệu phân loại hồ sơ |
| 5 | Số thứ tự văn bản trong hồ sơ | `DocOrdinal` | Số nguyên | Thứ tự của văn bản được sắp xếp trong hồ sơ |
| 6 | Tên loại văn bản | `TypeName` | Chuỗi ký tự | Tên loại văn bản (Quyết định, Công văn, Tờ trình...) |
| 7 | Số của văn bản | `CodeNumber` | Số nguyên | Số thứ tự văn bản đi do Văn thư cấp |
| 8 | Ký hiệu của văn bản | `CodeNotation` | Chuỗi ký tự | Ký hiệu viết tắt tên loại và cơ quan ban hành |
| 9 | Ngày, tháng, năm văn bản | `IssuedDate` | Ngày tháng | Ngày, tháng, năm ban hành văn bản |
| 10 | Tên cơ quan, tổ chức ban hành | `OrganName` | Chuỗi ký tự | Tên đầy đủ của cơ quan, tổ chức ban hành văn bản |
| 11 | Trích yếu nội dung | `Subject` | Văn bản | Tóm tắt nội dung chính của văn bản |
| 12 | Ngôn ngữ | `Language` | Chuỗi ký tự | Ngôn ngữ thể hiện văn bản (mặc định: `VN` hoặc `vi-VN`) |
| 13 | Số lượng trang của văn bản | `PageAmount` | Số nguyên | Tổng số trang văn bản |
| 14 | Ghi chú | `Description` | Văn bản | Ghi chú thêm về văn bản |
| 15 | Người ký | `SignerInfo` | Cấu trúc | Thông tin người có thẩm quyền ký văn bản: |
| | - Chức vụ người ký | `Position` | Chuỗi ký tự | Chức vụ của người ký |
| | - Họ và tên người ký | `FullName` | Chuỗi ký tự | Họ và tên đầy đủ của người ký |
| 16 | Nơi nhận | `To` | Danh sách | Danh sách cơ quan, tổ chức nhận văn bản: |
| | - Mã định danh cơ quan nhận | `OrganId` | Chuỗi ký tự | Mã định danh của cơ quan nhận văn bản |
| | - Tên cơ quan nhận | `OrganName` | Chuỗi ký tự | Tên cơ quan, tổ chức nhận văn bản |
| 17 | Mức độ khẩn | `Priority` | Chuỗi ký tự | Thường, Khẩn, Thượng khẩn, Hỏa tốc |
| 18 | Số lượng bản phát hành | `IssuedAmount` | Số nguyên | Số lượng bản phát hành |
| 19 | Hạn giải quyết | `DueDate` | Ngày tháng | Thời hạn giải quyết công việc được giao |

---

## III. BẢNG II: DỮ LIỆU THÔNG TIN ĐẦU VÀO CỦA VĂN BẢN ĐẾN

> Căn cứ Bảng II, Phần II, Phụ lục VI (Trang 75 - 76 Nghị định 30/2020/NĐ-CP):

| STT | Tên trường tiếng Việt | Tên trường tiếng Anh | Kiểu dữ liệu | Mô tả theo Nghị định 30 |
|:---:|-----------------------|:--------------------:|:------------:|-------------------------|
| 1 | Mã hồ sơ | `FileCode` | Chuỗi ký tự | Mã hồ sơ thu thập văn bản đến |
| 2 | Mã định danh cơ quan tiếp nhận | `OrganId` | Chuỗi ký tự | Mã định danh cơ quan nhận văn bản |
| 3 | Năm mục lục hồ sơ | `FileCatalog` | Số nguyên | Năm lập mục lục hồ sơ |
| 4 | Số và ký hiệu hồ sơ | `FileNotation` | Chuỗi ký tự | Ký hiệu hồ sơ thu thập |
| 5 | Số thứ tự văn bản trong hồ sơ | `DocOrdinal` | Số nguyên | Thứ tự văn bản trong hồ sơ |
| 6 | Tên loại văn bản | `TypeName` | Chuỗi ký tự | Tên loại văn bản đến |
| 7 | Số của văn bản đến | `CodeNumber` | Chuỗi ký tự | Số văn bản do cơ quan ban hành cấp |
| 8 | Ký hiệu của văn bản đến | `CodeNotation` | Chuỗi ký tự | Ký hiệu văn bản do cơ quan ban hành cấp |
| 9 | Ngày, tháng, năm văn bản | `PromulgationDate`| Ngày tháng | Ngày, tháng, năm ban hành ghi trên văn bản đến |
| 10 | Tên cơ quan ban hành văn bản | `OrganName` | Chuỗi ký tự | Tác giả phát hành văn bản |
| 11 | Trích yếu nội dung | `Subject` | Văn bản | Tóm tắt nội dung văn bản đến |
| 12 | Ngôn ngữ | `Language` | Chuỗi ký tự | Ngôn ngữ văn bản đến |
| 13 | Số lượng trang của văn bản | `PageAmount` | Số nguyên | Tổng số trang của văn bản đến |
| 14 | Ghi chú | `Description` | Văn bản | Ghi chú về văn bản đến |
| 15 | Ngày đến | `ReceiveDate` | Ngày tháng | Ngày tiếp nhận văn bản vào cơ quan |
| 16 | Số đến | `IncomingOrdinal` | Số nguyên | Số thứ tự văn bản đến do Văn thư cấp |
| 17 | Tác giả gửi văn bản | `From` | Cấu trúc | Thông tin cơ quan gửi: |
| | - Mã định danh cơ quan gửi | `OrganId` | Chuỗi ký tự | Mã định danh cơ quan gửi văn bản |
| | - Tên cơ quan gửi | `OrganName` | Chuỗi ký tự | Tên đầy đủ cơ quan gửi văn bản |
| 18 | Người ký văn bản đến | `SignerInfo` | Cấu trúc | Chức vụ (`Position`) và Họ tên (`FullName`) |
| 19 | Phân công giải quyết | `ProcessedInfo` | Cấu trúc | Thông tin phân công: |
| | - Đơn vị, người nhận xử lý | `Assignee` | Chuỗi ký tự | Phòng ban hoặc chuyên viên được giao xử lý |
| | - Hạn giải quyết | `DueDate` | Ngày tháng | Thời hạn giải quyết do Lãnh đạo ấn định |
| 20 | Mức độ khẩn | `Priority` | Chuỗi ký tự | Thường, Khẩn, Thượng khẩn, Hỏa tốc |

---

## IV. BẢNG III: DỮ LIỆU THÔNG TIN CỦA HỒ SƠ LƯU TRỮ ĐIỆN TỬ

> Căn cứ Bảng III, Phần II, Phụ lục VI (Trang 76 Nghị định 30/2020/NĐ-CP):

| STT | Tên trường tiếng Việt | Tên trường tiếng Anh | Kiểu dữ liệu | Mô tả theo Nghị định 30 |
|:---:|-----------------------|:--------------------:|:------------:|-------------------------|
| 1 | Mã hồ sơ | `FileCode` | Chuỗi ký tự | Mã hồ sơ lưu trữ |
| 2 | Tiêu đề hồ sơ | `Title` | Văn bản | Tên gọi khái quát nội dung hồ sơ |
| 3 | Năm mục lục hồ sơ | `FileCatalog` | Số nguyên | Năm lập mục lục hồ sơ |
| 4 | Số và ký hiệu hồ sơ | `FileNotation` | Chuỗi ký tự | Ký hiệu hồ sơ trong mục lục |
| 5 | Năm hình thành hồ sơ | `Year` | Số nguyên | Năm tài liệu được tập hợp vào hồ sơ |
| 6 | Thời hạn bảo quản | `Maintenance` | Chuỗi ký tự | Vĩnh viễn hoặc số năm cụ thể (5, 10, 20, 70 năm) |
| 7 | Chế độ sử dụng | `UsageMode` | Chuỗi ký tự | Hạn chế khai thác hoặc Sử dụng rộng rãi |
| 8 | Tổng số văn bản trong hồ sơ | `TotalDoc` | Số nguyên | Số lượng văn bản tài liệu trong hồ sơ |
| 9 | Tổng số trang của hồ sơ | `TotalPage` | Số nguyên | Tổng số trang tài liệu của toàn hồ sơ |
| 10 | Ghi chú | `Description` | Văn bản | Thông tin ghi chú thêm về hồ sơ |
| 11 | Thời gian bắt đầu | `StartDate` | Ngày tháng | Thời gian của văn bản sớm nhất trong hồ sơ |
| 12 | Thời gian kết thúc | `EndDate` | Ngày tháng | Thời gian của văn bản muộn nhất trong hồ sơ |

---

## V. NGUYÊN TẮC BẢO QUẢN AN TOÀN TÀI LIỆU ĐIỆN TỬ

1. **Sao lưu dữ liệu định kỳ:** Hệ thống tự động sao lưu dữ liệu văn bản và siêu dữ liệu tối thiểu hàng tuần và lưu trên ít nhất 02 phương tiện lưu trữ độc lập.
2. **Kiểm tra tính toàn vẹn:** Định kỳ quét mã băm (Hash SHA-256) để kiểm soát tính toàn vẹn của tệp văn bản, phát hiện mọi sự thay đổi trái phép.
3. **Bảo mật và Danh tính:** Mọi dữ liệu thử nghiệm, mẫu kiểm tra phải dùng placeholder chuẩn `[...]` thay vì các tên người thật.
