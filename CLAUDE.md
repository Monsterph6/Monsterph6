# Kho than — hệ thống quản lý kho than (thay thế sổ Excel)

Đây là điểm khởi đầu cho bất kỳ phiên Claude Code nào làm việc trong
repo này. Repo thay thế dần một hệ sinh thái ~15-20 file Excel liên
kết qua Power Query (đường dẫn tuyệt đối, dễ vỡ khi đổi máy) bằng 1
CSDL trung tâm + các module sinh báo cáo.

**Đọc trước khi code:**
- [`md/01-He_sinh_thai_du_lieu_Excel.md`](md/01-He_sinh_thai_du_lieu_Excel.md)
  — kết quả khảo sát toàn bộ file Excel nguồn, sheet, Power Query M
  code, đường dẫn phụ thuộc giữa các file. Đọc file này trước khi động
  vào bất kỳ module tổng hợp/báo cáo nào (Module 2 trở đi) để biết
  chính xác dữ liệu nguồn nằm ở đâu, cột nào, join với gì.
- `md/power_query/*.m` — M code gốc trích từ 4 workbook quyết toán,
  dùng để tra cứu công thức chính xác khi không chắc business logic.
- `kho_than_module/README.md` — tài liệu Module 1, đã hoàn thành.
- [`TASK.md`](TASK.md) — checklist tiến trình theo từng phase/module,
  **cập nhật file này mỗi khi bắt đầu/hoàn thành 1 bước hoặc khi 1
  quyết định "chưa chốt" ở đây được trả lời**. `CLAUDE.md` (file này)
  giữ lý do/kiến trúc; `TASK.md` giữ trạng thái "đang ở đâu, làm gì
  tiếp" — không trộn 2 việc vào 1 file.

## 1. Nghiệp vụ tóm tắt

Công ty kinh doanh than có nhiều **trạm** (kho: Tân Đức, Cống Câu, Cửa
Cấm, Vật Cách...). Mỗi trạm: nhập than thô/than mua → nhập kho theo
từng **chủng loại than** (vd "Cám 5a.1", "Cám 6b.1 ĐHD") → có thể
**phối trộn** (PA - phương án phối trộn) ra chủng loại khác → xuất
bán/xuất chuyển nội bộ. Cuối tháng: đối chiếu tồn, tính hao hụt, lập
biểu quyết toán theo mẫu công ty mẹ quy định (BM7, BM8, Quyết toán
KVCP, Cân bằng chất lượng than...).

Toàn bộ nghiệp vụ này hiện chạy bằng Excel: mỗi trạm 1 file NXT/tháng,
Power Query gộp lên các file tổng hợp, rồi lên các file quyết toán
cuối cùng. Vấn đề cố hữu (xem thêm README Module 1):
- Tồn kho là công thức chuỗi ô gắn số dòng tuyệt đối → sửa/xoá 1
  chứng từ giữa tháng làm sai toàn bộ dòng sau.
- Power Query trỏ **đường dẫn tuyệt đối trên máy cụ thể** (đã thấy
  nhiều query trỏ tới máy đã không còn dùng, vd
  `C:\Users\phamh\OneDrive - Cong ty CP Kinh doanh than Mien Bac -
  Vinacomin\...`) — vỡ ngay khi đổi máy/đổi người dùng OneDrive.
- **Tên than không đồng nhất**: cùng 1 loại than có thể được ghi khác
  nhau ở sổ trạm ("Cám 5a.1 ", "Cám 5a.1 (ĐHP)"), ở biểu 7, ở biểu 8,
  và ở "Cam_B8" (bảng ánh xạ riêng trong file Cân bằng chất) — ít nhất
  **3 bảng ánh xạ tên than khác nhau** rải rác trong 3 workbook khác
  nhau, không đồng bộ.

## 2. Mục tiêu kiến trúc

```
File Excel ngoại vi (chứng từ gốc)
        │  import (script Python, có dry-run + báo cáo tên than lạ)
        ▼
   CSDL trung tâm (SQLite mặc định, migrate được sang Postgres)
        │  query/service (tồn kho tính động, không lưu cứng)
        ▼
   Báo cáo định kỳ (xuất Excel/CSV đúng layout các biểu mẫu quyết toán)
```

Nguyên tắc giữ xuyên suốt mọi module (đã áp dụng ở Module 1, **bắt
buộc áp dụng tiếp** cho các module sau):
1. **CSDL là nguồn sự thật duy nhất.** Không module nào đọc thẳng
   file Excel của module khác — mọi liên kết đi qua CSDL, không đi
   qua đường dẫn file như Power Query hiện tại.
2. **Số liệu suy ra được bằng phép tính rẻ (SUM/window function trên 1
   bảng) thì không lưu cứng** — tồn kho theo (trạm, sản phẩm), số dư
   luỹ kế... vẫn tính động như Module 1 đang làm.
   **Ngoại lệ có chủ đích**: phân bổ (allocation) là bài toán khác
   hẳn, không nên tính động. Đã xác nhận qua file
   `QTTPT 2026\Tính tồn 2.xlsx` (xem mục 8 `md/01-...md`): việc phân
   bổ Tồn/HHB/HHKK **tổng theo sản phẩm** xuống **từng lô than cấu
   thành** (mỗi lô 1 Ak/Vk/Sk/Qk riêng, theo đẳng thức
   `L_B = L_TT + L_NT − L_T − L_HH − L_KK − L_XCN + L_NCN`) là 1 thuật
   toán phân bổ tuần tự qua nhiều lô (kiểu waterfall/FIFO), không phải
   1 SUM đơn giản — tính lại mỗi lần đọc sẽ tốn và không cần thiết.
   Với loại tính toán này: **lưu kết quả phân bổ thành 1 bảng snapshot
   theo kỳ** (`nam, thang, tram, san_pham` + chi tiết phân bổ theo
   lô), có cờ `da_chot` (đã chốt sổ). Quy tắc:
   - Kỳ **chưa chốt** (tháng hiện tại): có thể tính lại bất kỳ lúc
     nào khi dữ liệu nguồn (PA, kiểm kê...) thay đổi — có 1 action
     "tính lại phân bổ" tường minh, không tự động chạy ngầm mỗi lần
     đọc vì tốn.
   - Kỳ **đã chốt** (đã lập quyết toán): **không tự tính lại** khi có
     dữ liệu liên quan thay đổi sau đó — đúng tinh thần kế toán (số
     liệu kỳ đã chốt không được trôi ngầm). Muốn sửa phải có thao tác
     tường minh "mở lại kỳ" rồi tính lại.
   - Đây là mở rộng tự nhiên của pattern `ton_dau_ky` đã có ở Module 1
     (lưu tường minh 1 mốc, các kỳ sau tính tiếp từ đó) — không phải
     nguyên tắc mới, chỉ áp dụng cho lớp phân bổ/quyết toán thay vì
     lớp sổ chi tiết.
   - **Quy tắc làm tròn khi phân bổ — xác nhận 2026-07-10** (từ người
     dùng, đối chiếu đúng với sheet `Append1` của `Tính tồn 2.xlsx` —
     xem `md/01-...md` mục 8): sau khi tính lượng phân bổ thô cho từng
     dòng PA theo waterfall rồi làm tròn 2 chữ số, tổng các dòng đã
     làm tròn có thể lệch khỏi tổng thực tế 1 khoản nhỏ (bội số 0,01).
     Xử lý: tính `delta = giá_trị_đã_làm_tròn − giá_trị_gốc` cho từng
     dòng, xếp hạng theo `delta`; nếu tổng làm tròn thiếu → cộng 0,01
     lần lượt theo rank xuôi; nếu thừa → trừ 0,01 lần lượt theo rank
     ngược, tới khi khớp tổng thực. Biến thể của "phương pháp số dư
     lớn nhất". Đã xác nhận ở mức nguyên tắc, chi tiết cài đặt (tie-
     break, áp dụng cho cả 3 loại Tồn/HHKK/HHB hay riêng từng loại) để
     dành khi code Module 6.
3. **Import phải idempotent + có `--dry-run`.** Chạy lại 1 file Excel
   đã import trước đó không được tạo trùng dữ liệu.
4. **Dữ liệu kế toán không xoá cứng.** Soft delete (`deleted_at`) +
   audit log cho mọi bảng giao dịch tài chính, theo đúng mẫu
   `giao_dich_kho` / `giao_dich_audit_log` ở Module 1.
5. **Chuẩn hoá Unicode NFC khi đọc chuỗi từ Excel.** File Excel gốc có
   lẫn cả NFD lẫn NFC cho cùng 1 chữ có dấu — đã gặp lỗi thật ở Module
   1, xem `import_from_excel.py::nfc()`. Mọi script đọc Excel mới đều
   phải normalize NFC trước khi so khớp/lưu.
6. **Sửa lại khi bắt đầu code Module 3 (2026-07-08)**: ban đầu nguyên
   tắc này viết "mỗi module 1 thư mục riêng ở gốc repo" — **không còn
   đúng nữa**. Vì nguyên tắc #1 (1 CSDL chung) đòi hỏi mọi module dùng
   chung 1 `Base.metadata`/1 FastAPI app (Module 3 cần `Tram`/
   `SanPham`/gate tên than của Module 1/2 ngay trong cùng transaction),
   tách app riêng theo thư mục sẽ phá vỡ đúng nguyên tắc CSDL chung.
   **Thực tế đang làm**: `kho_than_module/` là **backend dùng chung
   duy nhất** cho mọi module — mỗi module thêm file riêng theo tên
   (`app/models_hang_nhap.py`, `app/services/hang_nhap.py`,
   `app/routers/hang_nhap.py`, `app/schemas_hang_nhap.py`...) thay vì
   thư mục gốc riêng, nhưng vẫn `import` chung `app/models.py::Base`
   nên chia sẻ đúng 1 CSDL/1 app. Ranh giới "module" giờ là ở **mức
   file/package trong `kho_than_module/`**, không phải ở mức thư mục
   gốc repo. `import_excel/` cũng dùng chung cho mọi luồng import của
   mọi module (`import_from_excel.py` cho Module 1,
   `import_hang_nhap_luong2.py` cho Module 3...).
7. **Bảng dữ liệu trên giao diện phải thao tác được kiểu Excel** —
   copy 1 vùng ô từ Excel rồi paste thẳng vào bảng trên phần mềm,
   khớp đúng theo hàng/cột đang chọn (không phải nhập tay từng ô).
   Đây là yêu cầu bắt buộc cho **mọi màn hình nhập/sửa dữ liệu dạng
   bảng** (sổ chi tiết, PA, hàng nhập, kết quả kiểm kê...), vì người
   dùng vẫn quen thao tác trên Excel và khối lượng dòng/tháng không
   nhỏ — bắt gõ tay từng ô là bước lùi so với Excel hiện tại.
   - Module 1 (`kho_than_module/frontend/index.html`) đang dùng
     **AG Grid Community** (miễn phí) — paste nhiều ô cùng lúc theo
     đúng vùng chọn (range paste) là tính năng của AG Grid
     Enterprise (trả phí), không có sẵn ở bản Community.
     **Đã chốt (2026-07-08, user không muốn tốn phí)**: **không** mua
     Enterprise — tự viết clipboard-paste handler (bắt sự kiện
     `paste`, tách dữ liệu theo tab/xuống dòng, đổ vào đúng ô bắt đầu
     từ ô đang chọn) chạy trên AG Grid Community, dùng chung cho mọi
     module có bảng nhập liệu thay vì viết lại mỗi nơi.
   - Đồng thời cũng nên hỗ trợ chiều ngược lại (copy từ bảng trong
     app dán ra Excel) để tiện đối chiếu, dù không bắt buộc bằng
     chiều paste-vào.
8. **Triển khai (deployment) — đã chốt (2026-07-08, thay quyết định
   Tailscale/self-host server trước đó — KHÔNG dùng phương án cũ)**:
   quy mô thực tế là **2 người dùng** (user + vợ), không cần server
   luôn bật. Mô hình: **local-first, đồng bộ tường minh qua cloud**,
   theo nguyên tắc nghiệp vụ **chỉ 1 người thao tác tại 1 thời điểm**
   (để khỏi phải giải quyết bài toán multi-writer thật, giữ chi phí
   $0).
   - Mỗi máy giữ **1 bản CSDL SQLite đầy đủ, local**. App chạy hoàn
     toàn offline sau khi đã tải dữ liệu về — không cần máy nào khác
     bật, không cần mạng khi đang làm việc.
   - Luồng dùng: mở app → app **tự kéo (pull)** bản mới nhất từ kho
     lưu trên cloud, ghi đè lên bản local → làm việc **offline** →
     xong việc, bấm **đẩy (push)** bản local lên cloud.
   - **KHÔNG được lặp lại đúng lỗi mà cả dự án này đang sửa** (đồng bộ
     ngầm, không ai biết ai đang cầm bản mới nhất, ghi đè mất dữ liệu
     của nhau) — bắt buộc có 2 lớp an toàn quanh pull/push, không làm
     "tải xuống - ghi đè lên" đơn giản:
     1. **Kiểm tra phiên bản trước khi push (optimistic concurrency).**
        Mỗi lần push lên cloud, kèm theo 1 số phiên bản/timestamp.
        App nhớ phiên bản đã pull lúc bắt đầu phiên làm việc; trước
        khi push, so với phiên bản hiện tại trên cloud — nếu khác
        (nghĩa là có người khác đã push xen giữa) thì **từ chối push
        đè**, báo lỗi rõ ràng, bắt pull lại rồi xử lý thủ công. Không
        bao giờ push đè âm thầm.
     2. **Khoá mềm hiển thị rõ ai đang giữ bản local để sửa.** Khi
        pull, app đánh dấu "đang được [tên người dùng] chỉnh sửa từ
        [giờ:phút ngày/tháng]" trên cloud; người thứ 2 mở app thấy
        ngay cảnh báo này **trước khi bắt đầu sửa** (không phải sau
        khi push mới biết bị từ chối) — để họ chủ động nhắn hỏi thay
        vì tự ý làm song song.
   - Nơi lưu bản cloud — 2 hướng khả thi, **chưa chốt kỹ thuật**, cần
     bàn khi bắt đầu code phần này:
     a) Vẫn dùng OneDrive/SharePoint đã có sẵn, nhưng app gọi
        **Microsoft Graph API để pull/push tường minh theo yêu cầu
        của người dùng** (không dựa vào tiến trình đồng bộ nền của
        OneDrive client — đó chính là nguồn gốc rủi ro đã phân tích ở
        lượt trước). Ưu điểm: không phát sinh dịch vụ mới, tận dụng
        hạ tầng đang trả tiền sẵn.
     b) Dịch vụ SQLite-cloud chuyên dụng (Turso/sqlitecloud.io, gói
        free tier) — có sẵn API pull/push, đỡ tự viết, nhưng thêm 1
        bên thứ 3 mới phải tin tưởng với dữ liệu kế toán.
   - Nên tách phần pull/lock/push thành 1 lớp riêng trong code (vd.
     `app/sync/`), không trộn vào logic nghiệp vụ — các service khác
     (`ton_kho.py`, `bao_cao.py`...) không cần biết dữ liệu đến từ
     đâu.

## 3. Ngân hàng tên than — thiết kế bắt buộc (yêu cầu cốt lõi)

**Vấn đề đã xác nhận qua khảo sát** (chi tiết ở mục 3 của
`md/01-He_sinh_thai_du_lieu_Excel.md`): hệ Excel hiện có ít nhất 2
bảng ánh xạ tên than độc lập, không đồng bộ với nhau:
- sheet `Tên cám` trong `Tổng hợp NXT các trạm 2026.xlsx`: `Than tại
  NXT → Biểu 8 / Biểu 7 / cờ TD / Tên TD`.
- named range `Cam_B8` trong `THP.Biểu mẫu Quyết toán KVCP 2026.xlsx`:
  `Cam_all → B8`, dùng riêng cho tính Cân bằng chất; dòng nào không
  khớp bị **âm thầm** tách ra một bảng lỗi (`Toncuoi (3)`) chứ không
  báo ai.

**Đã cài đặt (2026-07-08)** — xem `TASK.md` Phase 0.3 + Phase 1 để
biết chính xác file nào: bảng `san_pham_alias` + `ten_than_cho_duyet`,
`app/services/ten_than.py` (resolver dùng chung), gate trong
`import_from_excel.py` VÀ `app/services/hang_nhap.py` (Module 3 dùng
lại đúng service này, không viết lại), màn hình quản lý
`frontend/ten-than.html`. Còn thiếu: import dữ liệu alias khởi tạo từ
Excel cũ (`Tên cám`/`Cam_B8`), xử lý cờ `TD`.

**Mở rộng theo yêu cầu người dùng (2026-07-09)** — thiết kế giống đúng
hành vi thật của sheet `Tên cám` gốc trong `Tổng hợp NXT các trạm
<năm>.xlsx`:
- **So khớp không phân biệt hoa/thường + ký tự đặc biệt (dấu gạch
  ngang, non-breaking space)**: tài liệu mục này TỪNG ghi "so khớp
  không phân biệt hoa/thường" nhưng code CŨ chưa thực sự làm — đã sửa
  (`_khoa_so_khop()` trong `ten_than.py`). Đây là cách hệ thống TỰ
  nhận biết "tên than cũ viết sai" (dấu cách thừa, ký tự đặc biệt lạ,
  hoa/thường khác) mà KHÔNG cần con người can thiệp.
- **Gợi ý fuzzy-match cho tên chưa nhận diện**: khi 1 tên KHÔNG khớp
  tuyệt đối (dù đã chuẩn hoá) và rơi vào hàng đợi chờ duyệt, hệ thống
  tính độ giống (`difflib`) với các `san_pham` đã có và hiển thị gợi ý
  ngay trên `frontend/ten-than.html` — giúp người dùng nhận ra nhanh
  đây là lỗi gõ của 1 tên đã có (thay vì phải nhớ/tìm tay), nhưng
  **KHÔNG tự động gán** — quyết định cuối luôn là người dùng bấm xác
  nhận, tránh gộp nhầm 2 than thực sự khác nhau.
- **Reset đầu năm khác nhau theo nguồn gốc than** — xác nhận với người
  dùng: than **trong nước** (vd "Cám 4b.1 BT (tự doanh)") kế thừa
  nguyên qua các năm, không bao giờ tự ẩn; than **nhập khẩu** mỗi năm
  chỉ giữ lại sản phẩm CÒN TỒN, phần hết tồn bị ẩn (`active=False`,
  KHÔNG xoá cứng — đúng nguyên tắc #4) để danh mục gọn lại khi sang
  năm mới. Field mới `san_pham.nguon_goc` (`trong_nuoc`/`nhap_khau`)
  **ĐỘC LẬP với `co_tu_doanh`** (2 khái niệm khác nhau, không suy ra
  được từ nhau — đã xác nhận). Đây là **hành động tường minh** người
  dùng chủ động bấm (giống "chốt kỳ" Module 6), KHÔNG tự động chạy
  ngầm — xem `app/services/ten_than.py::reset_nam_moi_than_nhap_khau()`,
  `TASK.md` Phase 1.

**Thiết kế cho CSDL mới:**
- `san_pham` (đã có ở Module 1) là **danh mục chuẩn duy nhất** — mỗi
  chủng loại than thật chỉ có đúng 1 bản ghi.
- Thêm bảng `san_pham_alias` (module mới, hoặc mở rộng Module 1 nếu
  hợp lý hơn): `(id, san_pham_id, ngu_canh, ten_alias)` trong đó
  `ngu_canh` phân biệt loại tên: `nxt_tram` (tên ghi ở sổ trạm),
  `bieu_7`, `bieu_8`, `can_bang_chat`, `td` (tên khi là than tự
  doanh)... — thay cho việc mỗi workbook Excel tự có 1 bảng ánh xạ
  riêng. `UNIQUE(ngu_canh, ten_alias)` để 1 alias trong 1 ngữ cảnh chỉ
  trỏ về đúng 1 sản phẩm.
- **Gate bắt buộc khi import**: mọi script import từ file ngoại vi
  (NXT trạm, Hàng nhập, Sổ theo dõi PA...) khi gặp 1 tên than **không
  khớp được** với `san_pham.ten_sp`/`ma_sp` hoặc bất kỳ dòng nào trong
  `san_pham_alias` (sau khi đã NFC-normalize + trim + so khớp không
  phân biệt hoa/thường) thì:
  1. **Không tự tạo `san_pham` mới ngầm** (khác hành vi
     `_lay_hoac_tao` hiện tại trong `import_excel/import_from_excel.py`
     — cần sửa lại chỗ này khi làm tiếp Module 1, xem mục 5).
  2. Dừng dòng dữ liệu đó lại, gom vào danh sách "tên than chưa nhận
     diện" kèm ngữ cảnh (file nguồn, sheet, dòng).
  3. Trả danh sách này cho người dùng xác nhận: hoặc ánh xạ vào 1
     `san_pham` đã có (thêm alias mới), hoặc tạo `san_pham` mới tường
     minh. Có thể làm CLI tương tác hoặc 1 màn hình duyệt trong
     frontend — module nào import trước thì module đó cần cơ chế này,
     không để việc gõ tay tạo sản phẩm mới trôi qua không kiểm soát.
  4. Chỉ sau khi người dùng xác nhận, dữ liệu liên quan mới được ghi
     vào CSDL.

## 4. Hiện trạng — Module 1-6 đã xong phần lõi, Module 7-8 mới có 1 phần

Thay thế "Sổ chi tiết vật tư" (Nhập-Xuất-Tồn theo trạm, theo chủng
loại than). Đọc `kho_than_module/README.md` để biết đầy đủ. Trạng thái
cập nhật 2026-07-09 (chi tiết từng việc xem `TASK.md`):
- Backend FastAPI + SQLAlchemy, DB mặc định SQLite
  (`kho_than_module/kho_than.db`), migrate Postgres qua
  `DATABASE_URL`. **`kho_than_module/` giờ là backend dùng chung cho
  mọi module**, không riêng Module 1 nữa — xem nguyên tắc #6 đã sửa ở
  mục 2.
- Tồn kho tính động trong `app/services/ton_kho.py`, không lưu cột
  Tồn. **Đã sửa 1 lỗi nghiêm trọng**: `ton_dau_ky()` từng đệ quy vô
  hạn về quá khứ khi có giao dịch nhưng chưa từng khai báo `TonDauKy`
  tường minh — xem `TASK.md` mục 0.4 để biết chi tiết + test hồi quy.
- `import_excel/import_from_excel.py`: **đã sửa xong** — không còn
  auto-create `san_pham` ngầm nữa, đi qua gate ngân hàng tên than
  (mục 3) trước khi ghi CSDL.
- `pytest tests/ -v` **đã chạy thật**, 51/51 xanh (tăng dần theo module
  mới thêm) — xem `TASK.md` mục 0.4 danh sách lỗi thật đã tìm và sửa.
- `frontend/index.html` giờ **đã có** paste nhiều ô kiểu Excel (dòng
  trống cuối bảng + `frontend/js/excel-paste.js`, xem nguyên tắc #7
  mục 2) — tự viết, không dùng AG Grid Enterprise.
- `import_from_excel.py::parse_sheet()` **viết lại hoàn toàn (2026-07-08)**
  sau khi khảo sát ~1700 sheet thật — xem `TASK.md` Phase 0.4 chi tiết
  đầy đủ. Đổi API: giờ trả về `list[KetQuaImportSheet]` (không phải 1
  object) vì **44% sheet thật chứa nhiều hơn 1 sản phẩm khác nhau
  trong cùng 1 sheet**. Phụ phí BH/KC/Cân than/Cồn đống: nhãn phí nằm ở
  cột **Đơn giá** của các dòng nối tiếp 1 giao dịch Nhập (không phải
  cột TK đối ứng), gắn vào giao dịch cha **theo vị trí đọc** (không còn
  đoán "gần nhất cùng ngày"). **Đã xác nhận với người dùng**: cột "Ngày"
  dạng `"N"`/`"N-M"` là ngày thực hiện thật (N-M = phiên kéo dài 2
  ngày) — tháng lấy từ TÊN FILE, năm lấy từ TÊN THƯ MỤC cha, KHÔNG dùng
  ngày/tháng Excel tự đoán sai khi auto-convert chuỗi số nhỏ thành
  `datetime`. Kiểm chứng bằng số thật: khớp tuyệt đối với sheet "NXT"
  tổng hợp sẵn trong file Excel (cả trước và sau khi sửa cột Ngày); sau
  khi sửa, 0 dòng còn bị bỏ qua do "không đọc được Ngày" (trước đó mất
  ~15-20% giao dịch/tháng).
  **Đính chính quan trọng về vai trò 2 nguồn — xác nhận trực tiếp từ
  người dùng (2026-07-10)**: trước đây hiểu sheet `NXT` (trong mỗi file
  `NXT <Trạm> <tháng>.xlsx`) chỉ là nguồn **đối chiếu/kiểm chứng** cho
  số liệu parse từ "Sổ chi tiết vật tư" (`giao_dich_kho`). **Không
  đúng theo quy trình thật**: sheet `NXT` **là bảng tổng hợp do chính
  kế toán từng trạm tự lập** (không phải chỉ là 1 giá trị suy ra để
  kiểm tra) — công việc thật của người dùng (ứng với Module 5 "tổng
  hợp liên trạm") là **gộp lại các sheet `NXT` này giữa các trạm**,
  không phải tính lại từ sổ chi tiết vật tư. Nguyên văn xác nhận:
  *"sheet NXT trong từng file ấy là tổng hợp của các nhân viên kế
  toán, nhiệm vụ của tôi là tổng hợp lại. tôi chưa triển khai đến sổ
  chi tiết vật tư để tổng hợp."*
  **Ý nghĩa cho kiến trúc — cần sửa Module 5**: `tong_hop_lien_tram()`
  hiện tính TRỰC TIẾP từ `giao_dich_kho` (xem `TASK.md` Phase 4) —
  **không khớp đúng quy trình thật**. Nguồn chính thức cho "bảng NXT
  tổng hợp liên trạm" phải là **sheet `NXT` đọc trực tiếp từ từng file
  trạm** (cần thêm 1 import mới, chưa có), không phải suy ra từ giao
  dịch chi tiết. "Sổ chi tiết vật tư" → `giao_dich_kho` (Module 1) vẫn
  giữ nguyên giá trị riêng: lưu chứng từ chi tiết để **sau này in sổ
  chi tiết** (nguyên văn người dùng), và tiếp tục dùng để **đối chiếu
  chéo** với sheet NXT khi cần kiểm tra sai lệch — nhưng không còn là
  nguồn tính bảng NXT/tồn kho báo cáo chính. Cần cập nhật lại
  `app/services/tong_hop.py` khi code tiếp Module 5.
  Còn treo: join với
  `hang_nhap.bh/.kc/.vcbx/.phicanthan/.vun_gom` (Module 3) để đặt tên
  chính xác phụ phí khi cột Đơn giá không phải text (hiện vẫn đúng số
  tiền, chỉ ghi tạm "Phụ phí chưa rõ tên").
- Module 2 (`app/services/ten_than.py` + `frontend/ten-than.html`),
  Module 3 (`app/models_hang_nhap.py`, `app/services/hang_nhap.py`,
  `frontend/hang-nhap.html`), Module 4 (`app/models_phuong_an.py`,
  `app/services/phuong_an.py`, `frontend/phuong-an.html`) và Module 5
  (`app/services/tong_hop.py`, `frontend/tong-hop.html`) đã hoạt động
  được, sống chung trong `kho_than_module/` — xem mục 5 bảng roadmap
  và `TASK.md` để biết chính xác phần nào còn thiếu.
- **Module 6 (phân bổ Tồn/HHB/HHKK theo lô) vừa thêm phần lõi
  (2026-07-09)**: `app/models_phan_bo.py`, `app/services/phan_bo.py`,
  `frontend/phan-bo.html`. Thuật toán waterfall (Tồn → HHKK theo ngày
  kiểm kê → HHB phần còn lại) đã cài đặt đúng thứ tự xác nhận ở mục 8
  `md/01-...md`, có test hồi quy cho tính chất "1 lô PA dùng luỹ kế qua
  nhiều tháng". `L_XCN`/`L_NCN` (dùng trong công thức cân đối để gợi ý
  HHB) **đã chốt (2026-07-09): không map tự động vào 14 mã
  `loai_giao_dich`** — nhập tay khi có dữ liệu thật, y hệt cách `HHB`
  đang được nhập tay (xem mục 6 dưới) — KHÔNG còn là việc treo.
- **Module 7 (QTTPT) mới có 1 phần (2026-07-09)**:
  `app/services/quyet_toan.py::tinh_luong_ban_theo_lo()` +
  `frontend/quyet-toan.html` — tính lượng bán (L_B) THEO TỪNG LÔ, thay
  thế query `Bán`/`tenthan` của `QTTPT_2026.m`, dùng trực tiếp dữ liệu
  đã có từ Module 4 (PA) + Module 6 (Tồn/HHB/HHKK theo lô). `L_XCN`/
  `L_NCN` hard-code = 0 (chưa có nguồn — xem mục 6 dưới). **Đã chốt
  (2026-07-09): "giá vốn than" KHÔNG cần tự động hoá, user vẫn tính
  tay** — không phải việc treo nữa. **Còn thiếu thật**: sheet `CN`
  (nguồn thật XCN/NCN theo lô, có vài cột chưa xác nhận ý nghĩa), và
  layout xuất báo cáo `QTTPT 2026.xlsx` — xem `TASK.md` Phase 6 để biết chính xác
  còn thiếu gì.
- **Module 8 (cân bằng chất lượng) mới có phần lõi (2026-07-09)**:
  `app/services/can_bang_chat.py::can_bang_chat_theo_nhom_bm8()` +
  `frontend/can-bang-chat.html` — bình quân gia quyền Ak/Vk/Sk/Qk cho
  Tồn cuối/Nhập/Bán trong kỳ, gộp theo `nhom_bm8` (nhiều `san_pham`
  cùng nhóm), dùng dữ liệu đã có từ Module 4 + 6 + 7.
  **Đã đối chiếu `DCCL` bằng file thật (2026-07-10), khớp tuyệt đối**
  — xem `md/01-...md` mục 10b: layout `DCCL` = `Tháng | Thành phẩm |
  Than pha trộn | Lượng | AK | Vk | Qk | Sk`, đối chiếu 1 dòng thật
  (tháng 5, "Cám 6b.1 ĐHD" / "- Cám 5b.3") khớp tuyệt đối với khối cột
  **R-U** (không phải N-Q) của sheet `B8` trong `Cân bằng chất.xlsx` —
  xác định chính xác khối cột nào là kết quả cuối cùng trong số nhiều
  khối hiệu chỉnh liên tiếp của `B8`. Không còn "chưa đối chiếu được
  với số thật" nữa.
  **Phát hiện quan trọng (2026-07-10), đã đối chiếu bằng file thật**:
  quy trình thật KHÔNG dừng ở bình quân gia quyền đơn thuần — có thêm
  1 bước **hiệu chỉnh chất lượng từng cám thành phần cho khớp với
  `CLB` (chất lượng bán thực đo, từ chứng thư giám định)**, thực hiện
  **THỦ CÔNG theo kinh nghiệm** (xác nhận trực tiếp từ người dùng,
  không phải công thức cố định) — xem `md/01-...md` mục 9c. Kết quả
  hiệu chỉnh này (không phải bình quân gia quyền gốc) mới là dữ liệu
  cấp cho `DCCL`. `can_bang_chat.py` hiện tại **CHƯA có bước này** —
  cần thiết kế lại thành 1 bước gợi ý + xác nhận tay (cùng tính chất
  với `ĐN QÂ`/kết quả kiểm kê), không phải giá trị suy ra thuần tuý.
  Cũng đã giải mã được ý nghĩa cột `PL` trong sheet `CN`/`Bán2`: `PL`
  = `"TN"` (Trong Nước) / `"NK"` (Nhập Khẩu) — khớp thẳng field
  `san_pham.nguon_goc` đã có ở Module 2, xem mục 6 dưới (đã đóng điểm
  "chưa xác nhận" về sheet `CN`).
- **Bài học rút ra khi kiểm chứng Module 3/4 bằng dữ liệu thật**: đã
  có 1 lần suy luận sai từ đọc M code/mô tả gián tiếp (nhầm "Phí kẹp"
  với "Kẹp chì") mà không phát hiện ra cho tới khi chạy thử code thật
  trên file thật. **Khi có file Excel thật trong máy, luôn dry-run
  import script trên file đó trước khi coi là xong** — đáng tin cậy
  hơn hẳn chỉ test bằng file mẫu tự tạo hoặc tin vào việc đọc M code.

## 5. Các lớp dữ liệu & module cần xây tiếp

Xem sơ đồ đầy đủ + bằng chứng ở
`md/01-He_sinh_thai_du_lieu_Excel.md` mục 1. Tóm tắt roadmap theo
đúng thứ tự phụ thuộc dữ liệu (module sau cần dữ liệu của module
trước):

| # | Module (đề xuất thư mục) | Thay thế file Excel nào | Input | Output |
|---|---|---|---|---|
| 1 | `kho_than_module/` ✅ | `NXT\<tháng>\NXT <Trạm> <n>.xlsx` | Excel NXT từng trạm/tháng | Sổ chi tiết vật tư, tồn kho theo (trạm, sản phẩm) |
| 2 | ngân hàng tên than ✅ | sheet `Tên cám` (đã seed 2026-07-08, 223 `san_pham`), named range `Cam_B8` | — | `san_pham_alias` + cơ chế gate (mục 3) — còn thiếu: import `Cam_B8` (để dành Module 8) |
| 3 | hàng nhập ✅ | `HÀNG NHẬP\...\<lô hàng>.xlsx` (BKHN) + `Hàng nhập 2026.xlsx` | Chứng từ lô hàng nhập (hoá đơn, BB giám định, BB giao nhận) | Sổ hàng nhập theo trạm/tháng, giá vốn than nhập — cả 2 luồng đã chạy được, đã kiểm chứng luồng 1 với 97 file thật; còn thiếu: map nốt vài cột chưa xác nhận ở luồng 2 (KL TT, Đơn giá...) |
| 4 | phương án phối trộn (PA) ✅ | `Sổ theo dõi PA trạm 2026.xlsx` (sheet T1..T12) | Kế hoạch phối trộn: SPT, ngày HĐ/PT/NT, than vào/ra, Ak/Vk/Sk/Qk, khối lượng | Dữ liệu PA theo tháng, đầu vào cho tính hao hụt — đã kiểm chứng bằng 2322 dòng thật, còn thiếu: xác nhận công thức `L_B` với kế toán |
| 5 | tổng hợp liên trạm 🔶 cần sửa nguồn dữ liệu | Sheet `NXT` trong từng file `NXT <Trạm> <tháng>.xlsx` (KHÔNG phải tính lại từ sổ chi tiết — xác nhận 2026-07-10) | Sheet `NXT` của mọi trạm (tự kế toán trạm lập) | NXT gộp toàn công ty theo (trạm, chủng loại) — đầu vào cho BM7/BM8. **Đính chính (2026-07-10)**: `tong_hop_lien_tram()` hiện tính từ `giao_dich_kho` là SAI nguồn — phải đổi sang đọc thẳng sheet `NXT`, xem mục 4 dưới. `giao_dich_kho` (từ sổ chi tiết vật tư) giữ vai trò riêng: lưu chứng từ chi tiết để in sổ sau này + đối chiếu chéo |
| 6 | phân bổ Tồn/HHB/HHKK theo lô ✅ phần lõi | `QTTPT 2026\Tính tồn 2.xlsx` | Nhập tay: kết quả kiểm kê thực tế (Tồn, HHKK, HHB) theo (trạm, sản phẩm, tháng) + Module 4 (danh sách PA/lô) | Snapshot phân bổ theo kỳ: Tồn/HHB/HHKK chi tiết theo từng PA/lô, cờ đã chốt (thuật toán waterfall Tồn → HHKK → HHB đã cài đặt + test) — còn thiếu: kiểm chứng bằng dữ liệu thật, xác nhận nguồn L_XCN/L_NCN để tự tính tổng HHB (xem mục 4, mục 6 dưới) |
| 7 | quyết toán than pha trộn (QTTPT) 🔶 mới 1 phần | `QTTPT 2026\QTTPT 2026.xlsx` | Module 3 + Module 4 + Module 6 | Bán (✅ tính theo lô xong) — còn thiếu: đọc bảng `CN` thật vào CSDL (cấu trúc đã xác nhận đầy đủ 2026-07-10, xem mục 6 dưới — chỉ còn thiếu code import), layout xuất báo cáo. **Giá vốn than: đã chốt (2026-07-09) KHÔNG tự động hoá — user vẫn tính tay.** |
| 8 | cân bằng chất lượng 🔶 mới 1 phần | `Cân bằng chất.xlsx` (chính thức) → đích `THP.Biểu mẫu Quyết toán KVCP 2026.xlsx` sheet `DCCL` (xác nhận 2026-07-08) | Module 4 (Ak/Vk/Sk/Qk) + Module 6 + Module 7 | Bình quân gia quyền chất lượng than (✅ tính xong cho Tồn/Nhập/Bán) — còn thiếu: đối chiếu với sheet `DCCL` thật (chưa có file/M code để kiểm chứng) |
| 9 | biểu mẫu quyết toán tổng | `Quyết toán\Bao cáo NXT Biểu 07-TMB-print.xlsx` (BM7), `Quyết toán\Biểu 08 TMB-print.xlsx` (BM8), `THỐNG KÊ\Báo cáo NXT TD-CB (tháng)-print.xlsx` (BM PT/TD) — đích thật xác nhận 2026-07-08, xem mục 6 `md/01-...md` | Module 5, 7, 8 | Xuất Excel/PDF đúng layout: BM7 = NXT theo danh mục than (toàn công ty), BM8 = NXT theo trạm/cửa hàng, BM PT/TD = mẫu Tập đoàn tách Tự doanh/Pha trộn |

Không nhất thiết làm đúng thứ tự này nếu người dùng có ưu tiên khác —
nhưng **Module 2 (ngân hàng tên than) nên làm sớm**, vì mọi module
sau đều phụ thuộc vào tên than đã chuẩn hoá.

Module 6 (phân bổ) là lý do kỹ thuật cụ thể cho ngoại lệ "lưu snapshot
thay vì tính động" ở nguyên tắc #2 mục 2 — tách riêng khỏi Module 7
(QTTPT) vì (a) có sự kiện nhập liệu thủ công riêng (kết quả kiểm kê),
khác hẳn các module kia vốn chỉ import file, và (b) kết quả phân bổ
được cả Module 7 (giá vốn) lẫn Module 8 (chất lượng bình quân) dùng
chung — nếu nhét vào Module 7 thì Module 8 phải phụ thuộc ngược vào
Module 7, phá nguyên tắc mỗi module 1 việc.

### Module 3 (hàng nhập) — thiết kế 2 luồng, đã cài đặt xong (2026-07-08)

`ĐN QÂ` = **Quy ẩm đầu nguồn** — 1 **khối lượng** (tấn, cùng đơn vị với
`luong_HD`/`luong_NK`), KHÔNG phải phần trăm. **Công thức đã xác nhận**
(khớp đến từng đồng, kiểm chứng bằng 2 file thật độc lập cùng 1 lô
hàng — xem mục 5b `md/01-...md`):
```
hao_hut    = luong_CNchuaQA − ĐN_QÂ
hao_hut_qa = ĐN_QÂ − luong_HD
```
**Không phải than nào cũng cần ĐN QÂ** — chỉ than **nhập khẩu**; than
nội địa vốn dĩ không cần điền cột này, đây là thiết kế đúng chứ không
phải thiếu sót. **Đã xác nhận (2026-07-08): ĐN QÂ hiện điền tay, không
có nguồn tự động** — đây không phải khoảng trống tạm thời, mà là cách
làm việc thật, Module 3 không cần chờ/thiết kế thêm cho việc này.

**Đính chính (2026-07-10, kiểm chứng bằng 3 file BKHN thật + mã nguồn
`bkhn_td_gui.py` + file gộp thật)** — xem `md/01-...md` mục 5b để biết
đầy đủ:
- Mẫu BKHN **có sẵn cột quy ẩm cho cả than nội địa lẫn nhập khẩu**
  (không phải "than nội địa không có cột" như viết trước đây) — khác
  biệt thật chỉ là cột "Hao hụt quy ẩm" thường để trống ở dòng nội địa.
- Lý do ĐN QÂ phải nhập tay: đã đọc mã nguồn `bkhn_td_gui.py` và chạy
  thử `parse_file()` trên 2 file BKHN thật (1 nội địa, 1 nhập khẩu) —
  logic tự tính `hao_hutQA` của tool **luôn cho ra 0.0** ở cả 2 nhánh
  (1 nhánh hard-code 0, 1 nhánh bị lỗi trỏ trùng ô Excel khiến phép
  trừ ra 0 dù không phải vậy) — không đáng tin, nên người dùng phải tự
  đọc số liệu quy ẩm thật trong file rồi gõ tay. Phần tính phụ phí của
  tool (tiền than/VC/KC/BH/VCBX/cân than/vun gom) đã kiểm chứng khớp
  tuyệt đối, không có vấn đề.
- **"Phiếu điều chỉnh giá chỉ chỉnh tiền, không liên quan lượng"** —
  KHÔNG đúng cho mọi trường hợp. File thật `SK19 ĐC tăng lượng SIRIUS
  7.5.xlsx` là 1 phiếu điều chỉnh **tăng cả khối lượng** (147,5 tấn,
  chia 3 dòng con theo phương tiện, gắn vào các lô nhập đã có trước
  đó). Tool hiện tại (`bkhn_td_gui.py`) chỉ lấy đúng tổng tiền của
  loại phiếu này, bỏ qua lượng — **xác nhận đây là giới hạn có chủ
  đích của người dùng** (Excel hiện tại chỉ cần tổng, không cần tách
  theo lô con), không phải lỗi. **CHƯA CHỐT cho CSDL mới**: giữ hành
  vi cũ (ghi 0 lượng, chỉ tổng tiền) hay tách chi tiết theo lô con để
  cộng đúng lượng vào lô gốc — để người dùng quyết định khi làm Module
  3, xem mục 6 dưới.

Đã cài đặt (`app/services/hang_nhap.py`, `app/models_hang_nhap.py`,
`import_excel/import_hang_nhap_luong1.py`,
`import_excel/import_hang_nhap_luong2.py` — xem `TASK.md` Phase 2):

- **Vùng lưu nháp**: bảng staging riêng `hang_nhap_draft` (không phải
  file tạm trên đĩa — user chọn vậy để dễ quản lý bằng SQLAlchemy).

**Vai trò 2 luồng đã xác nhận rõ (2026-07-08) — quan trọng, khác cách
hiểu ban đầu:**
- **Luồng 2 (`import_hang_nhap_luong2.py`, đọc "Hàng nhập
  &lt;năm&gt;.xlsx") là đường nhập liệu CHUẨN, dùng cho MỌI trạm.**
  Các trạm khác ngoài Tân Đức (VC, VC2, TĐ2...) do cán bộ khác phụ
  trách, và họ **đã gửi dữ liệu về đúng theo format của file "Hàng
  nhập 2026.xlsx"** — tức KHÔNG cần Module 3 tự đọc file BKHN thô của
  từng trạm, cũng KHÔNG cần tổng quát hoá luồng 1 cho các trạm đó.
  Ghi thẳng không qua nháp (xem lý do ở trên). Cấu trúc: nhiều sheet
  T1..T12, header dòng 3, cột `HH`/`HHQA` đã tính sẵn — đã kiểm chứng
  đọc đúng 1312 dòng file thật.
- **Luồng 1 (`import_hang_nhap_luong1.py`, đọc file BKHN gốc) chỉ là
  1 TOOL HỖ TRỢ riêng cho trạm Tân Đức** (nơi `bkhn_td_gui.py` đang
  được dùng sẵn) — **không cần tổng quát hoá cho trạm khác**, vì các
  trạm khác đã đi qua luồng 2 rồi. 2 điểm vào:
  1. `import_folder()` — quét 1 thư mục file BKHN rời rạc. Đã kiểm
     chứng: 97 file thật đọc được, 0 lỗi.
  2. `import_file_da_gop()` (`--da-gop`) — đọc thẳng 1 file đã gộp
     (đầu ra `bkhn_td_gui.py`, dò cột theo TÊN vì cột "ĐN QÂ" chèn tay
     lệch vị trí giữa các file) — có ĐN QÂ thì chốt thẳng luôn.
  - `them_dong_luong_1()`/`chot_draft()`: thiếu `dn_qa` → nháp; có
    `dn_qa` → chính thức, hao_hut/hao_hut_qa **tự động tính lại**
    theo công thức trên.
  - Đã kiểm chứng end-to-end với file thật
    `HÀNG NHẬP T5.26-KD THAN TÂN ĐỨC.xlsx` — kết quả khớp chính xác.
- **Sheet `(DD)` (lô đang đi đường, chưa về kho)** — xác nhận: hiếm
  khi cần, khi cần thì nhập tay. `import_hang_nhap_luong2.py` **đã hỗ
  trợ sẵn** không cần sửa gì thêm: `doc_file(path, sheet="T5 (DD)")`
  (hoặc CLI `--sheet "T5 (DD)"`) đọc đúng 1 sheet `(DD)` cụ thể khi
  được yêu cầu tường minh — mặc định (không truyền `--sheet`) vẫn tự
  động bỏ qua mọi sheet `(DD)` để tránh tính nhầm hàng chưa về kho vào
  tồn.

## 6. Việc chưa xác nhận / cần hỏi người dùng trước khi code sâu

- **Đã xác nhận nguồn thật (2026-07-09)** — xem
  `md/power_query/QTTPT_2026.m` dòng 165-197: `L_XCN`/`L_NCN` **KHÔNG
  map vào 1 trong 14 mã `loai_giao_dich` của Module 1** — cả 2 đọc từ
  **CÙNG 1 sheet `CN` trong `QTTPT 2026.xlsx`** (Module 7, chưa khảo
  sát/xây), có dữ liệu **THEO TỪNG LÔ/PA cụ thể** (cột `Data.Column7` =
  lô, cùng shape với các sheet PA/HHKK/HHB khác trong file này: `SPT,
  N_HD, N_PT, N_NT, Tram, L_100, Ak, Vk, Sk, Qk, L_T, STTPA, Cảng,
  Tháng...`) — KHÁC HẲN Tồn/HHKK/HHB (vốn là **tổng theo kỳ**, cần
  waterfall phân bổ xuống lô). Query `XCN` lấy `L_T` đổi tên thành
  `L_XCN`, bỏ cột `C_CN`; query `NCN` cũng đọc sheet `CN` đó nhưng đổi
  vai trò 2 cột `Data.Column6`/`C_CN` cho nhau rồi lấy `L_T` thành
  `L_NCN` — gợi ý sheet `CN` ghi 1 dòng "chuyển nguồn" giữa 2 trạm/lô,
  1 bên đọc là Xuất (XCN) 1 bên đọc là Nhập (NCN) tại cùng 1 dòng dữ
  liệu (2 đầu 1 giao dịch chuyển). **Đã xác nhận trực tiếp từ người
  dùng (2026-07-10)**: sheet `CN` **chính là bảng GỘP (union) của
  X_CN và N_CN** — 2 tập dòng dữ liệu Xuất chuyển nguồn/Nhập chuyển
  nguồn nhập/lưu chung 1 sheet, không phải "2 cách đọc khác nhau của
  cùng 1 dòng" như suy đoán trên (đã sửa lại cách hiểu).
  **Ý nghĩa cho thiết kế**: khi làm Module 7 (QTTPT), cần thêm 1 nguồn
  nhập liệu riêng cho sheet `CN` này (tương tự Module 4 đọc PA — 1
  dòng/lô, không phải nhập tổng theo kỳ), rồi Module 6's
  `goi_y_hhb()`/`tinh_hhb_can_doi()` nên đổi từ nhận `xcn`/`ncn` dạng
  SCALAR nhập tay sang **SUM theo (trạm, sản phẩm, tháng) từ các dòng
  `CN` liên quan** — giống hệt cách `l_pa` hiện đang được sum từ các
  dòng `PhuongAn` trong `goi_y_hhb()`. **Chưa code phần đọc sheet `CN`
  này** (thuộc phạm vi Module 7, chưa bắt đầu) — thiết kế hiện tại của
  Module 6 (`KetQuaKiemKe.xcn`/`.ncn` nhập tay, mặc định 0) vẫn ĐÚNG làm
  bước đệm tạm thời cho tới khi Module 7 có bảng dữ liệu `CN` thật,
  không cần sửa gì ngay bây giờ. Xem `TASK.md` Phase 5 + Phase 6.
- **Đã xác nhận (2026-07-08)** — xem mục 6 `md/01-...md`: `KVCP` = Kho
  vận Cẩm Phả; `HHB` = Hao hụt bán; `HHKK` = Hao hụt kiểm kê; `XCN` =
  Xuất chuyển nguồn; `NCN` = Nhập chuyển nguồn; `THP` = **Than Hải
  Phòng** (tên công ty sở tại, không phải "Trạm Hải Phòng" như suy
  đoán ban đầu) — không dùng lại suy đoán cũ ở bất kỳ đâu khác trong
  repo. **Đã xác nhận (2026-07-08)**: `BM7` = Biểu 07-TMB (NXT theo
  danh mục/chủng loại than toàn công ty) → đích
  `Quyết toán\Bao cáo NXT Biểu 07-TMB-print.xlsx`; `BM8` = Biểu
  08-TMB (NXT chi tiết theo từng trạm/cửa hàng) → đích
  `Quyết toán\Biểu 08 TMB-print.xlsx`; ngoài ra còn `BM PT/TD` (mẫu
  Tập đoàn, TD=Tự doanh/PT=Pha trộn) → đích
  `THỐNG KÊ\Báo cáo NXT TD-CB (tháng)-print.xlsx` — cấu trúc cột chi
  tiết xem mục 6 `md/01-...md`. `QTTPT` = **Quyết toán than pha trộn**
  (KHÔNG phải "quyết toán tổn phí" như dùng nhầm trước đó trong repo —
  đã sửa lại tên Module 7 ở mọi nơi).
- ~~Công thức chính xác `L_B`...~~ **Đã xác nhận đầy đủ (2026-07-08)**
  — xem mục 4 `md/01-...md`: `L_TT` = tồn đầu kỳ, `L_TTN` = tồn cuối
  kỳ, `L_HHB` = hao hụt **bán**. Công thức
  `L_B = L_TT + L_PA − L_HHB − L_KK − L_TTN + L_NCN − L_XCN` là 1 cân
  đối kho chuẩn (suy từ `Tồn cuối = Tồn đầu + Nhập − Xuất − Hao hụt`),
  hợp lý về nghiệp vụ. (Thứ tự **phân bổ** Tồn/HHKK/HHB về từng PA thì
  đã xác nhận từ trước — xem mục 8 của `md/01-...md`: Tồn → PA gần
  nhất; HHKK → PA gần nhất so với ngày kiểm kê; HHB → phần PA còn lại,
  gần nhất lùi về trước.)
- Flow gộp file hàng nhập theo lô → `Hàng nhập 2026.xlsx`: **đã xác
  nhận đầy đủ** (tool `bkhn_td_gui.py`, thiết kế 2 luồng, công thức
  ĐN QÂ) — xem mục "Module 3 (hàng nhập)" ở mục 5 phía trên. Chỉ còn
  treo: **nguồn dữ liệu để lấy `ĐN QÂ` tự động** (công thức DÙNG nó
  thì đã xác nhận rồi) — người dùng sẽ cập nhật sau.
- ~~File `Cân bằng chất.xlsx`...~~ **Đã xác nhận (2026-07-08)**:
  `Cân bằng chất.xlsx` là bản **chính thức**, phục vụ trực tiếp cho
  `THP.Biểu mẫu Quyết toán KVCP 2026.xlsx` — thể hiện ở sheet `DCCL`
  của file THP KVCP (không phải `Bieu8 canbangchat` như suy đoán ban
  đầu). Cần cập nhật lại thiết kế Module 8 (mục 5 dưới) để dùng
  `DCCL` làm đích đối chiếu, không phải `Bieu8 canbangchat`.
- ~~Trạm khác ngoài Tân Đức... luồng 1 nên tổng quát hoá?~~ **Đã xác
  nhận (2026-07-08)**: KHÔNG cần. Các trạm khác (VC, VC2, TĐ2...) do
  cán bộ khác phụ trách và gửi dữ liệu về đúng theo format của
  `Hàng nhập <năm>.xlsx` (luồng 2) — luồng 1 (`import_hang_nhap_luong1.py`)
  chỉ giữ vai trò tool hỗ trợ riêng cho Tân Đức, nơi đang dùng sẵn
  `bkhn_td_gui.py`.
- ~~Sheet `(DD)`... chưa có module nào xử lý~~ **Đã xác nhận
  (2026-07-08)**: khi cần thì nhập tay qua luồng 2 với `--sheet "T5
  (DD)"` — code đã hỗ trợ sẵn (xem mục 5 phía trên), không cần module
  riêng. **Đính chính (2026-07-10)**: phát biểu "hiếm khi cần" **sai**
  — kiểm chứng bằng file thật `Hàng nhập 2026.xlsx`, riêng `T1 (DD)`
  đã có 23 dòng dữ liệu thật trong 1 tháng. Không đổi cách xử lý (vẫn
  nhập tay qua `--sheet`), chỉ sửa lại mức độ thường xuyên.
- **Bảng `CN` — ĐÃ GIẢI QUYẾT DỨT ĐIỂM (2026-07-10)**, xem `md/01-...md`
  mục 10a để biết đầy đủ. Tìm thấy đúng bảng thật (sheet `XCN` trong
  `QTTPT 2026.xlsx`, tên bảng Excel bên trong = `CN`), đủ 21 cột. Cơ
  chế: **1 dòng `CN` = 1 giao dịch chuyển nguồn**, chuyển `L_T` tấn
  của 1 thành phần (`Data.Column7`) từ đang tính vào sản phẩm `C_TP`
  (=`Data.Column6`) sang tính vào sản phẩm `C_CN` — ví dụ thật: chuyển
  từ "5a.10 ĐTB" (`C_CN`) sang "5a.10 ĐHP" (`C_TP`), đúng ý nghĩa
  "chuyển nguồn phục vụ phân loại theo đích bán" đã xác nhận ở mục
  trên. `C_PT` = nhãn đầy đủ thành phần kèm khoảng thời gian hiệu lực
  Ak; `C_B8` = bản rút gọn (bỏ khoảng thời gian); `PL`=TN/NK đã rõ từ
  trước. Không còn điểm treo nào ở bảng `CN` — sẵn sàng code Module 7
  đọc bảng này (1 dòng/lô, giống cách Module 4 đọc PA).
  Riêng `B_Ak`/`B_Vk`/`B_Qk`/`B_Sk`/`Round` — đối chiếu thêm sheet
  `Bán` thật trong `QTTPT 2026.xlsx` (không có 5 cột này) xác nhận đây
  là cột **chỉ có trong `Cân bằng chất.xlsx`** (tính thêm trên bản sao
  của `Bán`), không phải đầu ra chuẩn của Module 7 — công thức chính
  xác vẫn **CHƯA XÁC NHẬN** nhưng phạm vi ảnh hưởng đã thu hẹp (chỉ
  Module 8, không phải Module 7).
  2. **Đã xác nhận trực tiếp từ người dùng (2026-07-10)**: điều kiện
     `STTPA<0` trong query `Bán` của `THP_KVCP_2026.m` **lọc ra các
     cám thành phẩm đã pha trộn từ tồn năm trước** — tức những dòng
     không có 1 phương án (PA) thật trong năm hiện tại để đánh số
     `STTPA` (qua `Index` query, luôn ≥ 1), nên được gán 1 giá trị âm
     làm cờ đánh dấu "hàng tồn năm trước, không phải PA năm nay". Giải
     thích được vì sao công thức nhân `L_TTT` (tồn đầu kỳ) thay vì
     `L_B`: với nhóm hàng tồn năm trước này, "tồn đầu kỳ" mới là số
     lượng còn ý nghĩa để tính bình quân gia quyền chất lượng, không
     phải lượng bán trong năm. Không còn là điểm treo.
  3. **Đã xác nhận trực tiếp từ người dùng (2026-07-10)**: các named
     range `Bieu35a10`/`Bieu45a14` trong `THP_KVCP_2026.m` **là các
     biểu báo cáo riêng theo TỪNG CÁM THÀNH PHẨM** (Biểu 35 dành cho
     sản phẩm "5a.10", Biểu 45 dành cho "5a.14") — không phải mã
     trạm/khu vực như suy đoán ban đầu. Hậu tố `ĐHP`/`ĐTB`/`ĐVA` là
     phần của TÊN BIẾN THỂ sản phẩm (giống `ĐHD` ở "Cám 6b.1 ĐHD") —
     đã thấy đúng các tên này lặp lại xuyên suốt `LK`/`Result`/`CLB`/
     `Bán2` (vd "5a.10 ĐTB", "5a.14 ĐHP", "5a.14 ĐVA") làm tên `Cam_TP`
     (cám thành phẩm). **Đã xác nhận thêm ý nghĩa NGHIỆP VỤ (2026-07-10,
     từ người dùng)**: hậu tố `ĐHP`/`ĐTB`/`ĐVA` dùng để **biết bán cho
     đâu** — tức phân biệt cùng 1 chủng loại than (cùng khoảng Ak) theo
     **đích bán/kênh bán khác nhau**, không phải biến thể chất lượng
     hay kho vật lý. Cơ chế **chuyển nguồn (XCN/NCN) cũng phục vụ trực
     tiếp việc phân loại theo đích bán này** — khi 1 lô cần chuyển từ
     nguồn/trạm này sang phục vụ đích bán khác, ghi nhận qua XCN/NCN.
     Ý nghĩa chữ viết tắt cụ thể (`ĐHP`/`ĐTB`/`ĐVA`/`ĐHD` là viết tắt
     của đích bán/khách hàng nào) vẫn **CHƯA XÁC NHẬN**, nhưng không
     ảnh hưởng thiết kế `san_pham` (chỉ cần lưu đúng chuỗi tên, không
     cần giải mã từng chữ viết tắt).
  4. Phiếu "điều chỉnh" khi có cả lượng thay đổi (không chỉ tiền) —
     xem mục "Module 3" phía trên — CSDL mới nên ghi tổng (như Excel
     hiện tại) hay tách theo lô con: **cần người dùng quyết định**.
  5. ~20 sheet ẩn chưa rõ vai trò trong `Hàng nhập 2026.xlsx` (`LastM`,
     `CBC`, `TD`, `CB`, `TH`, `TH thang`, `CL nhập`, `Nhap1`...) và 3
     sheet ẩn trong `Tính tồn 2.xlsx` (`PAKK`, `PL`, `Sheet1`) — không
     ảnh hưởng luồng chính đã xác nhận, nhưng chưa rõ có dữ liệu/công
     thức nào cần dùng lại hay không.
