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

## Cấu hình sẵn trong repo

- **Script ID (GAS)**: `15XwGNzoptOO8D6VcH4G1hFV0fWkdWfdz8aF6T0YqDlVYdC-VLlDWAVbd` — đã khai báo trong `.clasp.json`.
- **Database (Google Sheet)**: `SPREADSHEET_ID` ở đầu `Code.gs` đang để **trống** — app tự tạo một Spreadsheet riêng trong Drive khi chạy lần đầu. (Sheet `12E1CJQdwsYrTvlXrBYprtBQqZNjDGVpcRXjbFxc2GlQ` từng được thử gán cứng nhưng thuộc tài khoản khác, script không có quyền ghi — nên đã bỏ, xem lại lịch sử version nếu cần đổi.)
- **GitHub Pages**: `https://monsterph6.github.io/Monsterph6/` (nhánh `gh-pages`) là một **vỏ PWA tĩnh** — trang chỉ chứa `index.html` + `manifest.json` + `sw.js` + icon, nhúng web app GAS thật sự bên trong qua `<iframe>`. Xem mục **"Kết nối GitHub Pages ↔ GAS"** bên dưới trước khi tạo deployment mới.

## Cách 1 — Đẩy code lên GAS bằng clasp (khuyên dùng)

Yêu cầu: đã cài [Node.js](https://nodejs.org). Chạy trong thư mục repo này:

```bash
npm install -g @google/clasp
clasp login          # đăng nhập tài khoản Google sở hữu script
clasp push -f        # đẩy Code.gs, SeedData.gs, Index.html, appsscript.json lên GAS
```

> Nếu `clasp push` báo lỗi *"User has not enabled the Apps Script API"*: mở <https://script.google.com/home/usersettings>, bật **Google Apps Script API**, chờ ~1 phút rồi chạy lại.

Sau khi push xong, mở <https://script.google.com> → dự án của bạn → **Triển khai** → **Tùy chọn triển khai mới** → **Ứng dụng web** (xem bước 3–4 bên dưới).

## Kết nối GitHub Pages ↔ GAS — QUY TẮC BẮT BUỘC khi deploy

`https://monsterph6.github.io/Monsterph6/` (nhánh `gh-pages`) là một PWA shell tĩnh — file
`index.html` trong đó nhúng thẳng URL của **một deployment GAS cụ thể** qua `<iframe>`:

```
https://script.google.com/macros/s/AKfycbwj0feG3ubQU--ls_nLP8C2w-FQkx2Lx2MbeoeD50vEJVmbW7hpjhtafl2_1CFslwGT/exec
```

Deployment ID này (`AKfycbwj0feG...`) **phải giữ nguyên vĩnh viễn** — mỗi lần đưa code mới lên GAS,
**không được tạo deployment mới** (`clasp deploy` không kèm `-i`), vì sẽ sinh ra URL khác và làm
GitHub Pages bị kẹt ở bản cũ. Luôn luôn cập nhật **vào đúng ID cũ**:

```bash
clasp push -f
clasp deploy -i AKfycbwj0feG3ubQU--ls_nLP8C2w-FQkx2Lx2MbeoeD50vEJVmbW7hpjhtafl2_1CFslwGT \
  --description "Mô tả ngắn thay đổi lần này"
```

Nhờ vậy URL nhúng trong `gh-pages/index.html` không bao giờ cần sửa lại — trang GitHub Pages
tự động lấy đúng bản mới nhất mỗi lần build lại. Nếu vô tình đã tạo deployment mới (lỡ quên
`-i`), chạy `clasp deployments` để tìm ID thừa và xoá bằng `clasp undeploy <deploymentId>`.

## Cách 2 — Dán tay (khoảng 5 phút)

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

> App dùng Google Sheet có ID khai báo ở hằng `SPREADSHEET_ID` (đầu tệp `Code.gs`) làm cơ sở dữ liệu; tài khoản triển khai cần có quyền chỉnh sửa file Sheet đó. Nếu để `SPREADSHEET_ID = ''`, app sẽ tự tạo một Spreadsheet mới trong Drive ở lần chạy đầu. Nút **📄 Mở Google Sheet** trong app dẫn thẳng tới Sheet đang dùng.

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
