# Ứng dụng Gia phả & Văn khấn (Google Apps Script)

Ứng dụng web chạy trên Google Apps Script, dữ liệu đọc/ghi trực tiếp từ Google Sheets.

## Chức năng

- Quản lý **thành viên gia phả**: thêm người, lưu quan hệ cha/mẹ qua ID, xem danh sách và cây gia phả.
- Khi chọn cha/mẹ trong form, hệ thống hiển thị theo định dạng **ID - Tên** để dễ chọn, nhưng vẫn lưu ID chuẩn vào Sheet.
- Ở phần ngày sinh/ngày mất có thể chọn nhập theo **Âm lịch** hoặc **Dương lịch**; hệ thống tự chuyển đổi và lưu **đồng thời cả ngày Âm + ngày Dương**.
- Quản lý **văn khấn**: thêm tiêu đề/chủ đề/nội dung, lưu và hiển thị danh sách.
- Tự động tạo 2 sheet với header chuẩn:
  - `ThanhVien`:
    - `id`, `hoTen`, `ngaySinhDuong`, `ngaySinhAm`, `ngayMatDuong`, `ngayMatAm`, `gioiTinh`, `idCha`, `idMe`, `ghiChu`
  - `VanKhan`:
    - `id`, `tieuDe`, `chuDe`, `noiDung`, `ghiChu`

## Cấu trúc file

- `Code.gs`: API backend, xử lý dữ liệu Sheet, chuyển đổi ngày Âm/Dương.
- `Index.html`: giao diện web app.
- `appsscript.json`: cấu hình Apps Script project.

## Cách triển khai

1. Tạo Google Spreadsheet mới.
2. Mở **Extensions > Apps Script**.
3. Copy nội dung file vào project Apps Script tương ứng:
   - `Code.gs`
   - `Index.html`
   - `appsscript.json` (Project Settings > Show "appsscript.json")
4. Deploy:
   - **Deploy > New deployment > Type: Web app**
   - Execute as: `Me`
   - Who has access: theo nhu cầu (ví dụ `Anyone with link`)
5. Mở URL web app để sử dụng.

## Gợi ý sử dụng

- Khi thêm thành viên, lấy giá trị `ID` trong bảng để liên kết `ID cha`/`ID mẹ` cho đời sau.
- Nếu đang có sheet cũ, app sẽ tự nâng cấp header theo chuẩn mới khi chạy lần đầu.
