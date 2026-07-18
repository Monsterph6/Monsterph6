# MU Auto Bãi SS21 — Tự động chạy bãi theo tọa độ (MU Online Season 21 / Fast Mu)

App auto **chạy bãi theo tọa độ** cho MU Online **Season 21** — thiết kế cho lối chơi **bằng chuột**
của SS21 và server dạng **Fast Mu có reset / grand reset**.

> ⚠️ Công cụ này chỉ gửi chuột/phím ở mức ứng dụng (không can thiệp bộ nhớ game).
> Một số server cấm auto ngoài — hãy kiểm tra luật server trước khi dùng. App chạy trên **Windows**.

---

## Cách hoạt động (SS21)

SS21 chơi bằng chuột: **chuột trái = di chuyển**, **chuột phải = đánh skill tại con trỏ**, và game có
sẵn **MU Helper** (auto trong game, bật/tắt bằng phím `Home`) tự đánh + nhặt đồ + uống pot.

App này đóng vai **người canh tọa độ + quản lý reset**:

```
 ┌──────────────────────────────────────────────────────────────┐
 │  OCR đọc tọa độ X,Y trên màn hình                            │
 │    ├─ Lệch khỏi bãi → TẮT MU Helper → chuột trái đi về bãi   │
 │    └─ Tới bãi       → BẬT MU Helper (Helper lo đánh/nhặt/pot)│
 │  OCR đọc LEVEL                                               │
 │    └─ Đủ level → gõ /reset → đếm đủ mốc → /grandreset        │
 │                → /move về map → chạy lại bãi                 │
 └──────────────────────────────────────────────────────────────┘
```

### 2 chế độ đánh
| Chế độ | Mô tả |
|--------|-------|
| **MU Helper** (khuyên dùng) | App chỉ canh tọa độ và bật/tắt Helper đúng lúc. Đánh, nhặt đồ, uống pot do Helper trong game lo — **nhớ cấu hình Helper trước** (icon cạnh mini-map hoặc phím `Z`). |
| **Chuột phải** | App tự đánh: chuột phải (skill) xoay quanh nhân vật theo 8 hướng. Dùng khi server không có/không muốn dùng Helper. |

### Tính năng
- 🧭 Chạy bãi theo tọa độ, tự quay lại khi lệch, tự lách khi bị kẹt
- 🧮 **Tự hiệu chỉnh hướng đi**: camera MU là isometric nên hướng X/Y game ≠ ngang/dọc màn hình —
  bấm nút **"Hiệu chỉnh hướng đi (auto)"**, app tự click thử 2 hướng, đọc tọa độ đổi thế nào và tính ra ma trận hướng
- ♻️ **Auto reset / grand reset** (cho Fast Mu): đọc level bằng OCR → đủ level gõ `/reset`,
  đếm số lần reset → đủ mốc gõ `/grandreset`, xong `/move` về map và chạy lại bãi
- ⚔️ Đánh bằng chuột phải hoặc phối hợp MU Helper
- 🧪 Auto HP/MP theo màu pixel (tùy chọn — mặc định tắt vì Helper đã lo)
- ⌨️ Hotkey toàn cục `F8` bật/tắt, `F9` dừng khẩn cấp

---

## Cài đặt

1. Cài **Python 3.10+**: https://www.python.org/downloads/ (tick *Add Python to PATH*).
2. Cài **Tesseract-OCR** (đọc tọa độ + level): https://github.com/UB-Mannheim/tesseract/wiki
   (mặc định `C:\Program Files\Tesseract-OCR\tesseract.exe`).
3. Chạy `run.bat` **bằng quyền Administrator** (lần đầu tự cài thư viện).

---

## Thiết lập lần đầu (5 bước)

1. **Vùng OCR tọa độ** (tab *Bãi / Tọa độ*): tìm ô hiển thị `X, Y` trên màn hình game.
   Dùng nút **"Lấy tọa độ chuột"** (tab Chính) lấy góc trên-trái → nhập `L,T,W,H`.
   Bấm **"Test đọc tọa độ (OCR)"** đến khi đọc đúng.
2. **Hiệu chỉnh hướng đi**: đứng chỗ trống trong game → bấm **"Hiệu chỉnh hướng đi (auto)"**.
   App click thử 2 hướng và tự tính ma trận. Bấm **"Lưu config"**.
3. **Set bãi**: nhập `Tọa độ X/Y đích` + bán kính (tab *Bãi / Tọa độ*).
4. **Chọn chế độ đánh** (tab *Đánh quái*): để **MU Helper** nếu server có Helper
   (cấu hình Helper trong game trước — skill, range, nhặt đồ, pot).
5. **Auto reset** (tab *Reset*, tùy chọn): set vùng OCR level (test bằng nút **"Test đọc level"**),
   level reset (vd 400), lệnh reset của server bạn (vd `/reset`), lệnh về map (vd `/move tarkan`).
   Muốn grand reset tự động thì bật thêm và khai số lần reset cần (vd 100).

Xong bấm **F8** để chạy. App chờ 3 giây để bạn đưa chuột vào cửa sổ game.

---

## Lưu ý & xử lý sự cố
- **Không gửi được chuột/phím vào game** → chạy bằng **Administrator**; thử để game ở chế độ **windowed**.
- **OCR sai** → thu nhỏ vùng OCR ôm sát con số; số phải rõ nét trên nền tối.
- **Nhân vật đi sai hướng** → chạy lại "Hiệu chỉnh hướng đi (auto)" (mỗi lần đổi góc camera/độ phân giải nên hiệu chỉnh lại).
- **Helper bị lệch trạng thái** (app tưởng đang bật mà game đã tắt — vd sau khi chết):
  bấm `Home` thủ công 1 lần cho khớp, hoặc F8 tắt/bật lại app.
- **Lệnh reset của server khác** (`/reset auto`, `/xoadiem`, …) → sửa ở tab Reset cho khớp server bạn.
- Số lần reset được **lưu tự động** vào `config.json` (`resets_done`) nên tắt app không mất.

---

## Cấu trúc file
```
muauto.py             # App chính (GUI + bot)
config.example.json   # Cấu hình mẫu (app tạo config.json khi bạn bấm Lưu)
requirements.txt      # Thư viện
run.bat               # Chạy nhanh trên Windows
```
