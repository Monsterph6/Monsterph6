# MU Auto Bãi SS21 — Tự động chạy bãi theo tọa độ (MU Online Season 21 / Fast Mu)

App auto **chạy bãi theo tọa độ** cho MU Online **Season 21** — thiết kế cho lối chơi **bằng chuột**
của SS21 và server dạng **Fast Mu có reset / grand reset**.

> ⚠️ Công cụ này chỉ gửi chuột/phím ở mức ứng dụng (không can thiệp bộ nhớ game).
> Một số server cấm auto ngoài — hãy kiểm tra luật server trước khi dùng. App chạy trên **Windows**.

---

## Cách hoạt động (SS21 / FASTMU)

SS21 chơi bằng chuột: **chuột trái = di chuyển**, **chuột phải = đánh skill tại con trỏ**.
Nhiều server (như FASTMU) đã **đóng MU Helper** và bot trong game đòi VIP — app này auto từ bên ngoài:

```
 ┌──────────────────────────────────────────────────────────────────┐
 │  Chọn đúng CỬA SỔ MU trong danh sách (hỗ trợ mở nhiều acc)       │
 │  Đọc TITLE cửa sổ:  [Char: X] [Level: 400 + 451] [RR: 14 / GR:0] │
 │    └─ Level đủ → gõ /reset → RR đủ mốc → /grandreset             │
 │                → /move về map → chạy lại bãi                     │
 │  OCR đọc tọa độ X,Y (góc trên trái: "Lorencia 143,131")          │
 │    ├─ Lệch khỏi bãi → chuột trái đi về bãi (ma trận isometric)   │
 │    └─ Tới bãi       → chuột phải đánh skill xoay quanh nhân vật  │
 │  Canh 2 quả cầu HP/MP theo màu → tự uống pot                     │
 └──────────────────────────────────────────────────────────────────┘
```

### Điểm mạnh với client FASTMU
- **Level / RR / GR đọc trực tiếp từ title cửa sổ** — chính xác 100%, không cần OCR.
- **Chọn cửa sổ game từ danh sách** (kèm tên process .exe) — không sợ nhầm khi mở nhiều cửa sổ;
  mọi vùng OCR/click tính **tương đối theo cửa sổ**, kéo cửa sổ đi đâu vẫn chạy đúng.

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

## Thiết lập lần đầu (6 bước)

1. **Chọn cửa sổ MU** (tab *Chính*): chọn đúng cửa sổ game trong danh sách (có tên .exe kèm theo),
   bấm **"Làm mới"** nếu chưa thấy. Bấm **"Test title (Level/RR/GR)"** — phải hiện đúng
   `Char/Level/RR/GR` của bạn.
2. **Vùng OCR tọa độ** (tab *Bãi / Tọa độ*): mặc định đã set cho client FASTMU 1280×986
   (ô `Lorencia 143,131` góc trên trái). Bấm **"Test đọc tọa độ (OCR)"** — nếu sai thì chỉnh
   `L,T,W,H` (tọa độ **tương đối theo cửa sổ game**).
3. **Hiệu chỉnh hướng đi**: đứng chỗ trống trong game → bấm **"Hiệu chỉnh hướng đi (auto)"**.
   App click thử 2 hướng, đọc tọa độ đổi thế nào và tự tính ma trận. Bấm **"Lưu config"**.
4. **Set bãi**: nhập `Tọa độ X/Y đích` + bán kính (tab *Bãi / Tọa độ*).
5. **Chế độ đánh** (tab *Đánh quái*): để **Chuột phải** (FASTMU đã đóng MU Helper).
   Chọn sẵn skill muốn đánh trong game (skill đang gắn chuột phải).
6. **Auto reset** (tab *Reset*): level reset (400), lệnh reset của server (vd `/reset`),
   lệnh về map sau reset (vd `/move tarkan`). Grand reset: bật + khai mốc RR (app đọc RR từ title).

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
