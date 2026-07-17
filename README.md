# MU Auto Bãi — Tự động chạy bãi theo tọa độ (MU Online / Fast Mu)

App tự động **chạy bãi theo tọa độ** cho MU Online (Fast Mu và các server private khác).
Nó đọc tọa độ nhân vật trên màn hình bằng OCR, tự đi về bãi bạn đã set, đánh quái, nhặt đồ,
tự uống HP/MP và quay lại bãi khi bị lệch.

> ⚠️ **Lưu ý:** Đây là công cụ gửi phím/chuột ở mức ứng dụng (không can thiệp bộ nhớ game).
> Một số server cấm dùng auto — bạn tự chịu trách nhiệm và nên kiểm tra luật của server trước khi dùng.
> App chạy trên **Windows** (MU là game DirectX).

---

## Tính năng
- 🧭 **Chạy theo tọa độ:** đọc X,Y của nhân vật bằng OCR → tự đi về bãi đã set, giữ trong bán kính.
- ⚔️ **Auto đánh:** spam phím skill theo chu kỳ (hoặc giữ phím).
- 🎒 **Auto nhặt đồ** theo phím pickup.
- 🧪 **Auto HP/MP:** đọc màu thanh máu/mana, tự uống khi tụt dưới ngưỡng.
- ✨ **Auto buff** định kỳ.
- ⌨️ **Hotkey toàn cục:** `F8` bật/tắt, `F9` dừng khẩn cấp.
- 🖥️ **Giao diện** để chỉnh và lưu cấu hình, có nút lấy tọa độ chuột & test thanh máu.

---

## Cài đặt

1. Cài **Python 3.10+**: https://www.python.org/downloads/ (nhớ tick *Add Python to PATH*).
2. Cài **Tesseract-OCR** (để đọc tọa độ): https://github.com/UB-Mannheim/tesseract/wiki
   - Mặc định cài vào `C:\Program Files\Tesseract-OCR\tesseract.exe`.
   - Nếu bạn **không muốn dùng OCR**, tắt ô "Bật đọc tọa độ OCR" — app vẫn auto đánh/pot/nhặt và
     định kỳ click về giữa màn hình để giữ vị trí.
3. Chạy `run.bat` (lần đầu nó tự `pip install -r requirements.txt`).
   - Nên **chạy bằng quyền Administrator** để hotkey toàn cục và gửi phím vào game hoạt động.

Hoặc thủ công:
```bat
pip install -r requirements.txt
python muauto.py
```

---

## Cách chỉnh cho đúng server của bạn

### 1) Vùng OCR đọc tọa độ (tab **Bãi / Tọa độ**)
- Trong MU thường có ô hiển thị tọa độ (vd `130, 130`). Xác định khung chữ nhật bao quanh số đó.
- Nhập `Vùng OCR [L,T,W,H]` = `left,top,width,height` (pixel màn hình).
  - Mẹo: dùng nút **"Lấy tọa độ chuột"** ở tab Chính — rê chuột tới góc trên-trái của ô tọa độ,
    giữ 3s để lấy `L,T`; ước lượng `W,H` cho vừa chữ.
- `Tọa độ X/Y đích`: tọa độ bãi bạn muốn đứng.
- `Bán kính`: cho phép lệch bao nhiêu ô trước khi đi về.
- `Bước đi`: mỗi lần đi, app click cách tâm màn hình bao nhiêu pixel (90 là hợp lý).

> Không có/không đọc được ô tọa độ? Tắt OCR, app sẽ dùng chế độ "về giữa màn hình" định kỳ.

### 2) Phím & chu kỳ (tab **Săn quái**)
- `Phím đánh`: ví dụ `e` (một hoặc nhiều phím cách nhau dấu phẩy: `e,r`).
- `Phím nhặt đồ`, `Phím buff` theo phím bạn đã gán trong game.

### 3) Auto HP/MP (tab **HP/MP**)
- `Pixel HP bar X/Y`: tọa độ **một điểm** nằm giữa thanh máu (khi máu đầy điểm đó có màu đỏ).
  - Dùng "Lấy tọa độ chuột" để lấy, rồi bấm **"Test đọc HP/MP"** để xem % ước lượng.
- `Ngưỡng HP/MP` (0..1): tụt dưới ngưỡng thì uống. Vd `0.55` = uống khi máu dưới 55%.
- `full_color` / `empty_color` trong `config.json`: màu RGB lúc đầy và lúc cạn của thanh — chỉnh nếu
  server dùng skin thanh máu khác.

---

## Hotkey
| Phím | Chức năng |
|------|-----------|
| `F8` | Bật / Tắt auto |
| `F9` | Dừng khẩn cấp (panic) |

Sau khi bấm bật, app chờ `start_delay_sec` giây (mặc định 3s) để bạn đưa chuột vào cửa sổ game.

---

## Xử lý sự cố
- **Không gửi được phím vào game:** chạy app bằng **Administrator**. MU là DirectX nên app dùng
  `pydirectinput`; nếu vẫn không được, thử chạy game ở chế độ **cửa sổ / windowed**.
- **OCR đọc sai số:** chỉnh lại vùng OCR ôm sát số hơn; đảm bảo chữ tọa độ rõ, nền tối. Có thể chỉnh
  ngưỡng nhị phân trong hàm `ocr_coords`.
- **Uống pot sai lúc:** bấm "Test đọc HP/MP" để soi %; chỉnh lại pixel X/Y hoặc `full/empty_color`.
- **Hotkey không ăn:** thư viện `keyboard` cần quyền Admin; hoặc dùng nút trong giao diện.

---

## Cấu trúc file
```
muauto.py             # App chính (GUI + bot loop)
config.example.json   # Cấu hình mẫu (app tự tạo config.json khi bạn lưu)
requirements.txt      # Thư viện cần cài
run.bat               # Chạy nhanh trên Windows
```

Chỉnh xong nhớ bấm **"Lưu config"** để ghi ra `config.json`.
