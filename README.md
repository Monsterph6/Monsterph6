# 🏮 App Gia phả — Chi họ Phạm Hiếu (Google Apps Script)

Web app gia phả xây dựng trên **Google Apps Script (GAS)**, dữ liệu lưu trong **Google Sheet**.
Dữ liệu gốc được trích từ file Excel *"Phả đồ chi họ Phạm Hiếu làng Liễu Điện, xã Cao Minh, huyện Vĩnh Bảo"* — gồm **7 đời, 55+ thành viên**, kèm ngày giỗ âm lịch.

## Tính năng

- **Phả đồ tương tác**: cây gia phả đủ 7 đời, kéo–thả, phóng to/thu nhỏ (chuột lăn hoặc 2 ngón trên điện thoại), nút "vừa màn hình".
- **Thẻ thành viên**: tên, đời thứ, chức danh (Tiên tổ, Cao tổ, Chi trưởng, Tổ cô...), ngày giỗ, vợ/chồng hiển thị ngay trong thẻ.
- **Danh sách theo đời**: bảng liệt kê từng thế hệ kèm quan hệ (con cụ nào, vợ/chồng cụ nào).
- **Lịch giỗ**: tự động gom toàn bộ ngày giỗ, sắp xếp theo tháng/ngày âm lịch.
- **Tìm kiếm** không dấu (gõ "hieu dieu" vẫn tìm ra "Hiếu Điều"), tự cuộn đến thẻ tìm thấy.
- **Thêm / sửa / xóa** thành viên ngay trên web (thêm con, thêm vợ/chồng cho từng cụ) — hoặc sửa trực tiếp trong Google Sheet.
- **In** phả đồ.
- Lần chạy đầu app **tự tạo Google Sheet** và đổ sẵn toàn bộ dữ liệu từ phả đồ gốc.

## Cài đặt (khoảng 5 phút)

1. Mở <https://script.google.com> → **Dự án mới** (New project). Đặt tên, ví dụ *Gia phả họ Phạm Hiếu*.
2. Tạo đủ 4 tệp và dán nội dung tương ứng từ repo này:
   | Tệp trong repo | Tạo trong Apps Script |
   |---|---|
   | `Code.gs` | tệp Script có sẵn `Code.gs` (dán đè) |
   | `SeedData.gs` | ➕ → **Tập lệnh** (Script), đặt tên `SeedData` |
   | `Index.html` | ➕ → **HTML**, đặt tên `Index` |
   | `appsscript.json` | Bật ⚙️ *Cài đặt dự án* → "Hiển thị tệp kê khai appsscript.json", rồi dán đè |
3. Bấm **Triển khai** (Deploy) → **Tùy chọn triển khai mới** → loại **Ứng dụng web**:
   - *Thực thi bằng*: **Tôi** (Me)
   - *Ai có quyền truy cập*: **Bất kỳ ai** (Anyone) — để cả họ xem không cần đăng nhập; hoặc chọn hẹp hơn tùy ý.
4. Bấm **Triển khai**, cấp quyền khi được hỏi (app cần quyền tạo/đọc Google Sheet), rồi mở **URL ứng dụng web** — xong! Gửi link này cho mọi người trong họ.

> Lần đầu mở app, một Spreadsheet tên **"Dữ liệu Gia phả — Chi họ Phạm Hiếu"** sẽ xuất hiện trong Google Drive của bạn. Đó là "cơ sở dữ liệu" của app — nút **📄 Mở Google Sheet** trong app dẫn thẳng tới đây.

## Cấu trúc dữ liệu (sheet `GiaPha`)

| Cột | Ý nghĩa |
|---|---|
| `ID` | Mã số duy nhất của mỗi người |
| `HoTen` | Họ tên |
| `GioiTinh` | Nam / Nữ |
| `Doi` | Đời thứ mấy (1 = Tiên tổ) |
| `ChaID` | ID của cha/mẹ trong họ (quan hệ huyết thống) |
| `VoChongCuaID` | Nếu là dâu/rể: ID của người phối ngẫu trong họ |
| `NgayGio` | Ngày giỗ âm lịch, dạng `ngày/tháng` (vd `18/12`) |
| `NamSinh`, `NamMat` | Năm sinh / mất (nếu biết) |
| `ChucDanh` | Tiên tổ, Cao tổ, Chi trưởng, Tổ cô, Ngành trưởng... |
| `GhiChu` | Ghi chú tự do |
| `ThuTu` | Thứ tự anh chị em trong nhà |

Sửa dữ liệu trong Sheet xong chỉ cần tải lại trang web là phả đồ cập nhật. Muốn quay về dữ liệu gốc từ phả đồ Excel, chạy hàm `resetToSeed` trong trình soạn Apps Script (⚠️ ghi đè toàn bộ Sheet).

## Ghi chú về dữ liệu trích từ phả đồ

Quan hệ cha–con được đọc theo **đường kẻ nối** trên phả đồ Excel gốc, ví dụ:

- Đời 3: cụ **Phạm Trung Hiền** nối xuống từ cụ **Phạm Hiếu Chân** (Cao tổ nhánh 2).
- Đời 6: cụ Tạo là con cụ Luật; cụ Huyến, Toản là con cụ Toan; cụ Xá, Sướng và cụ bà (mẹ cụ Cộng, cụ Cư) là con cụ Tuyên.

Một vài vị trí phả đồ gốc không vẽ rõ (đã ghi chú ngay trong cột `GhiChu` để họ tộc xác minh):

- Cụ **Phạm Thị Hiên** (cạnh cụ Tửu) và cụ **Phạm Thị Hằng** (cạnh cụ Sinh Huy): chưa rõ là vợ hay con.
- Cụ **Phạm Thị Thu** (cạnh cụ Thao Lược) và ô ghi **"Mầm con"**: cần xác minh.
- Cụ bà đời 6 phả đồ chỉ ghi *"Mẹ cụ Cộng, cụ Cư"* — chưa rõ tên húy.

Các con số sau tên trong phả đồ gốc (vd `(18-12)`) được hiểu là **ngày giỗ âm lịch** và đưa vào cột `NgayGio`.
