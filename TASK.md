# TASK.md — Tiến trình xây dựng app quản lý kho than

Checklist tiến trình, cập nhật liên tục qua các phiên làm việc — đánh
dấu `[x]` khi xong (ghi ngày), thêm ghi chú nếu có quyết định/vướng
mắc phát sinh lúc code mà chưa có trong `CLAUDE.md`. File này trả lời
**"đang ở đâu, làm gì tiếp"**; lý do/kiến trúc đằng sau mỗi bước xem
`CLAUDE.md` — không lặp lại nội dung đó ở đây.

## Trạng thái tổng quan

| Phase | Nội dung | Trạng thái |
|---|---|---|
| 0 | Hạ tầng dùng chung + hoàn thiện Module 1 | ✅ Xong phần lõi (2026-07-08) — trừ 0.1 (hoãn) |
| 1 | Module 2 — ngân hàng tên than (đầy đủ) | ✅ Xong (2026-07-09) — thêm reset đầu năm than nhập khẩu + gợi ý fuzzy-match; còn thiếu import `Cam_B8` (để dành Module 8) |
| 2 | Module 3 — hàng nhập | ✅ Xong (2026-07-08) — cả 2 luồng đã kiểm chứng bằng file thật |
| 3 | Module 4 — phương án phối trộn (PA) | ✅ Xong (2026-07-08) — đã kiểm chứng bằng 2322 dòng thật |
| 4 | Module 5 — tổng hợp liên trạm | ✅ Service/API/frontend xong (2026-07-08) — Module 1 (parser) đã viết lại + kiểm chứng bằng số thật, sẵn sàng import dữ liệu nhiều trạm |
| 5 | Module 6 — phân bổ Tồn/HHB/HHKK theo lô | ✅ Xong phần lõi (2026-07-09) — test bằng dữ liệu tự tạo, chưa kiểm chứng bằng dữ liệu thật |
| 6 | Module 7 — quyết toán than pha trộn (QTTPT) | 🔶 Mới có 1 phần: tính lượng bán (L_B) theo lô (2026-07-09) — giá vốn KHÔNG cần làm (user tính tay); XCN/NCN thật/layout xuất báo cáo chưa làm |
| 7 | Module 8 — cân bằng chất lượng | 🔶 Mới có phần lõi: bình quân gia quyền Ak/Vk/Sk/Qk (2026-07-09) — chưa đối chiếu sheet DCCL thật |
| 8 | Module 9 — biểu mẫu quyết toán tổng | ⏳ Chưa bắt đầu |

83/83 test tự động (`pytest tests/ -v` trong `kho_than_module/`) xanh
tính đến 2026-07-09, bao gồm test cho Module 2 (mở rộng), 3, 4, 5, 6,
7, 8 (phần lõi). Đã chạy server thật trên **CSDL dev thật đang dùng**
(`kho_than.db`, có 223 `san_pham` seed thật) để kiểm chứng migration
nhẹ `_them_cot_thieu_sqlite()` tự thêm cột `nguon_goc` không lỗi, API
`/api/danh-muc/san-pham` vẫn trả đúng dữ liệu cũ. Smoke test qua server
`uvicorn` thật (không chỉ TestClient) đã xác nhận cả 8 trang frontend (`index.html`, `ten-than.html`,
`hang-nhap.html`, `phuong-an.html`, `tong-hop.html`, `phan-bo.html`,
`quyet-toan.html`, `can-bang-chat.html`) và API đều phục vụ đúng —
riêng `phan-bo.html`/`quyet-toan.html`/`can-bang-chat.html` mới
smoke-test qua `curl` (`phan-bo.html`: lưu kiểm kê → gợi ý HHB → tính
phân bổ → chốt kỳ → từ chối tính lại → mở lại kỳ;
`quyet-toan.html`: seed PA + phân bổ → gọi API lượng bán;
`can-bang-chat.html`: seed PA + phân bổ → gọi API bình quân gia quyền
— cả 2 kết quả khớp tính tay), CHƯA tự bấm qua trình duyệt thật.

**Đã kiểm chứng bằng dữ liệu thật** (không chỉ file mẫu tự tạo) — hiếm
khi làm được ở giai đoạn sớm, đáng tin cậy hơn hẳn test mẫu đơn thuần:
- Import luồng 1 hàng nhập: chạy dry-run cả 97 file thật trong
  `HÀNG NHẬP\T5\HÀNG NHẬP T5.26` — 0 file lỗi.
- Import PA: chạy dry-run `Sổ theo dõi PA trạm 2026.xlsx` (cả 12 sheet
  T1-T12) — xử lý đúng 2322 dòng hợp lệ.
- Seed ngân hàng tên than: chạy thật `seed_ten_cam.py` với
  `Tổng hợp NXT các trạm 2026.xlsx` — đọc 272 dòng, tạo đúng 223
  `san_pham` (49 dòng trùng sau chuẩn hoá, khớp dry-run trước khi ghi).
- `import_from_excel.py` viết lại hoàn toàn sau khi dry-run file trạm
  thật lật ra 5 lỗi thật + 1 phát hiện lớn về cấu trúc (44% sheet chứa
  nhiều sản phẩm) — xem Phase 0.4. **Kiểm chứng bằng số**: sản phẩm
  "Cám 5a.1" tính từ `NXT Tân Đức 3.xlsx` khớp tuyệt đối với sheet
  "NXT" (Power Query tổng hợp có sẵn trong chính file) — tồn đầu kỳ
  6362.63, tổng nhập 12059.67, khớp đến 2 số thập phân.
- Quá trình này lật ra 1 lỗi tài liệu (nhầm "Phí kẹp" với "Kẹp chì" —
  đã sửa trong `md/01-...md`) — bài học: **luôn kiểm chứng bằng file
  thật khi có thể, đừng chỉ tin suy luận từ M code hoặc sample tự tạo**.
- **Đợt kiểm chứng mới (2026-07-10)** — người dùng cung cấp trực tiếp
  6 file thật + mã nguồn `bkhn_td_gui.py`, đọc bằng `openpyxl` và chạy
  thử logic tool thật (không chỉ đọc M code/tài liệu). Kết quả đầy đủ
  đã cập nhật vào `CLAUDE.md` mục "Module 3" + mục 6, và `md/01-...md`
  mục 5b/5c/5e/8. Tóm tắt các đính chính quan trọng:
  1. Mẫu BKHN có cột quy ẩm cho **cả** than nội địa lẫn nhập khẩu
     (không phải "nội địa không có cột" như ghi trước đây).
  2. Lý do ĐN QÂ phải nhập tay: `parse_file()` của `bkhn_td_gui.py`
     luôn cho `hao_hutQA=0.0` ở cả 2 nhánh xử lý (1 hard-code, 1 lỗi
     trỏ trùng ô) — đã xác nhận bằng cách chạy lại logic thật trên 2
     file BKHN thật (SK01 nội địa, SK02 nhập khẩu).
  3. "Phiếu điều chỉnh giá chỉ chỉnh tiền" — sai với 1 loại phiếu
     thật (`SK19 ĐC tăng lượng...`, có điều chỉnh cả 147,5 tấn lượng).
     Tool hiện tại chỉ giữ tổng tiền cho loại này (giới hạn có chủ
     đích, người dùng xác nhận) — CSDL mới cần quyết định có tách chi
     tiết theo lô con hay không.
  4. Công thức ĐN QÂ (`hao_hut = luong_CNchuaQA − ĐN_QÂ`, `hao_hut_qa
     = ĐN_QÂ − luong_HD`) được xác nhận thêm 2 lần độc lập nữa (dòng
     HĐ=2 trong `Hàng nhập 2026.xlsx` khớp tuyệt đối; dòng HĐ=1007
     trong `HÀNG NHẬP T5.26-KD THAN TÂN ĐỨC.xlsx` khớp đúng số đã ghi
     trước đó) — độ tin cậy công thức giờ rất cao (4 lần kiểm chứng
     độc lập).
  5. Cấu trúc `Hàng nhập 2026.xlsx` (header 33 cột dòng 3, cơ chế
     VLOOKUP Biểu 8/Biểu 7/TD/TD-PT từ `NXT` qua sheet `Tên cám`, cấu
     trúc `T<n> (DD)`) đã kiểm chứng khớp đúng bằng số thật.
  6. `Tính tồn 2.xlsx`: đính chính vai trò `LK` (là **đầu vào**, không
     phải bảng trung gian như ghi trước đây) + xác nhận `Result`/
     `CheckKQ`/`Append1` bằng số thật + ghi nhận **quy tắc làm tròn
     phân bổ mới** (rank theo delta làm tròn, bù 0,01) do người dùng
     cung cấp trực tiếp — chưa từng có trong tài liệu cũ.
  - Còn treo (chưa xác nhận, đã ghi vào `CLAUDE.md` mục 6): ý nghĩa
    cột `C_TP`/`C_PT`/`PL`/`C_B8` trong sheet `CN`; điều kiện
    `STTPA<0` trong query `Bán` của `THP_KVCP_2026.m`; mã `ĐHP`/`ĐTB`/
    `ĐVA`; vai trò ~20 sheet ẩn mới thấy trong `Hàng nhập 2026.xlsx` và
    3 sheet ẩn (`PAKK`/`PL`/`Sheet1`) trong `Tính tồn 2.xlsx`.

---

## Phase 0 — Hạ tầng dùng chung + hoàn thiện Module 1

Làm trước tiên: mọi module sau đều phụ thuộc lớp đồng bộ, gate tên
than, và UI paste-Excel.

### 0.1. Lớp đồng bộ cloud (`CLAUDE.md` nguyên tắc #8)
- [ ] **Hoãn theo quyết định của user (2026-07-08)** — code phần local
      trước, làm lớp đồng bộ sau khi rõ nhu cầu thực tế hơn. Không có
      việc nào trong mục này được làm ở lượt code này.

### 0.2. Clipboard-paste kiểu Excel cho AG Grid (`CLAUDE.md` #7) ✅
- [x] `frontend/js/excel-paste.js` — module dùng chung, thuần logic
      (không phụ thuộc AG Grid API cụ thể ngoài `getFocusedCell`),
      dùng lại được cho Module 3 và các module sau
- [x] Áp dụng vào `frontend/index.html`: 5 dòng trống cuối bảng sổ chi
      tiết gõ/dán được, nút "Lưu các dòng mới" gọi `POST
      /api/giao-dich/bulk` (endpoint mới, 1 transaction, huỷ cả lô
      nếu 1 dòng lỗi)
- [ ] Chiều copy ngược lại (app → Excel) — **chưa làm**, không bắt
      buộc bằng chiều paste-vào theo nguyên tắc #7

### 0.3. Ngân hàng tên than — phần lõi (`CLAUDE.md` mục 3) ✅
- [x] Bảng `san_pham_alias` + `ten_than_cho_duyet` (`app/models.py`,
      `schema/schema_sqlite.sql`, `schema/schema_postgres.sql`)
- [x] `app/services/ten_than.py`: `chuan_hoa()`, `tim_san_pham()`,
      `ghi_nhan_ten_chua_nhan_dien()`, `resolve_hoac_cho_duyet()`
- [x] `import_excel/import_from_excel.py`: bỏ hẳn auto-create qua
      `_lay_hoac_tao` cho `SanPham` — thay bằng gate qua
      `ten_than_svc`; sheet có tên chưa nhận diện bị BỎ QUA hoàn toàn
      (không tạo `san_pham`/`giao_dich_kho`), ghi vào hàng đợi
- [x] CLI tương tác: `--xac-nhan-ten-than` sau khi import, duyệt tên
      than ngay trên terminal (gán alias hoặc tạo mới)
- [x] Test: `tests/test_import.py::test_import_chan_ten_than_chua_nhan_dien`
      — xác nhận chặn đúng, không tạo trùng hàng đợi khi import lại,
      và import thành công sau khi "duyệt" thủ công

### 0.4. Nợ kỹ thuật Module 1 (`CLAUDE.md` mục 4 / README Module 1)
- [x] Cài `requirements.txt`, chạy thật `pytest tests/ -v` — **tìm ra
      và sửa 4 lỗi thật** (không có lỗi nào trong 4 lỗi này liên quan
      tới nghiệp vụ phụ phí, đều là lỗi kỹ thuật):
      1. `schemas.py`: `Decimal` serialize thành **chuỗi** JSON thay
         vì số (pydantic v2 mặc định) — sửa bằng kiểu `So` dùng
         `PlainSerializer` chung cho mọi field số.
      2. `import_from_excel.py`: tạo `Tram`/`SanPham` qua
         `_lay_hoac_tao()` flush() ngay sau khi tạo, **trước khi** gán
         cột NOT NULL (`ten_tram`/`ten_sp`) → vỡ ràng buộc DB. Sửa:
         không flush trong `_lay_hoac_tao()` nữa, caller tự flush sau
         khi gán đủ cột bắt buộc (áp dụng cả cho `DoiTuong`, chưa bị
         test bắt nhưng cùng lỗi).
      3. **Nghiêm trọng** — `app/services/ton_kho.py::ton_dau_ky()`:
         đệ quy lùi vô hạn về quá khứ khi có giao dịch nhưng CHƯA
         từng khai báo `TonDauKy` tường minh ở bất kỳ tháng nào (điều
         kiện dừng cũ kiểm tra "có dữ liệu tồn tại" toàn cục thay vì
         "có dữ liệu TRƯỚC thời điểm đang xét" — luôn đúng một khi đã
         có 1 giao dịch, nên không bao giờ dừng cho tới khi chạm
         ngưỡng an toàn `_depth>1200` và ném `RecursionError`). Sửa
         bằng cách tính "thời điểm sớm nhất có dữ liệu" làm điểm chặn
         đệ quy thật sự. Phát hiện qua test bulk-create mới, không
         phải test cũ nào (mọi test cũ đều tình cờ khai báo tồn đầu kỳ
         tường minh trước). Xem test hồi quy
         `test_ton_kho.py::test_ton_dau_ky_khong_co_ban_ghi_tuong_minh_van_khong_de_quy_vo_han`.
      4. `POST /api/giao-dich/bulk` (mới thêm — xem 0.2): không
         `rollback()` tường minh khi 1 dòng giữa lô lỗi, dựa nhầm vào
         việc đóng Session sẽ tự rollback — đúng trong production
         (mỗi request 1 Session riêng) nhưng có thể rò rỉ dữ liệu nửa
         vời trong ngữ cảnh Session dùng chung nhiều request (đã gặp
         khi viết test). Sửa: `try/except: db.rollback(); raise`
         tường minh ngay trong endpoint.
- [x] **Xác nhận được BẰNG DỮ LIỆU THẬT (2026-07-08, không cần hỏi kế
      toán nữa cho phần này)** — người dùng chỉ đúng ví dụ cụ thể (kho
      Tân Đức, tháng 3, lô "Than Anthracite Lào - Lô hàng 06/T03/2026
      (Tàu GOLDEN STAR)", số HĐ 680): đối chiếu sheet "GOLDEN STAR"
      trong `NXT Tân Đức 3.xlsx` với dòng số HĐ=680 trong sheet `T3`
      của `Hàng nhập 2026.xlsx` — **khớp tuyệt đối từng đồng**:
      `Tiền than`=3.170.394.291, `BH`=1.424.849, `KC`=329.077,
      `VCBX`=6.213.118, `Cân than`=1.321.940, `Vun gom`=1.784.610.
      2 phát hiện quan trọng từ đối chiếu này:
      1. **Nhãn phụ phí (BH/KC/Cân than/Cồn đống) nằm ở cột "Đơn giá"
         của dòng tiếp theo, KHÔNG nằm ở cột "TK đối ứng"** như
         `import_from_excel.py::MA_PHU_PHI_MAC_DINH` đang giả định —
         "TK đối ứng" giữ NGUYÊN mã đối tác (vd `331`) xuyên suốt cả
         khối nhiều dòng của 1 giao dịch Nhập; nhãn phí chỉ xuất hiện ở
         cột Đơn giá của các dòng nối tiếp không có Lượng. **Logic phát
         hiện phụ phí hiện tại vì vậy gần như KHÔNG BAO GIỜ khớp đúng
         trên dữ liệu thật** (rà toàn bộ `NXT/Tháng *.2026/*.xlsx` chỉ
         thấy phụ phí ở dạng này, 0 trường hợp TK đối ứng literal =
         "BH"/"KC" có số tiền khác 0).
      2. **Không cần "đoán" gắn phụ phí vào giao dịch Nhập gần nhất
         nữa** — số liệu ĐÃ CÓ SẴN, tách đúng theo lô, trong
         `hang_nhap.bh`/`.kc`/`.vcbx`/`.phicanthan`/`.vun_gom` (Module
         3, đã import qua luồng 2). Cách đúng: khi đọc "Sổ chi tiết vật
         tư" (Module 1) gặp 1 khối Nhập, gắn/đối chiếu với bản ghi
         `hang_nhap` cùng trạm + số HĐ/phương tiện (khớp text, vd
         "PT: HP 4852" ↔ `phuong_tien`) thay vì tự tính lại từ các dòng
         "Đơn giá" rời rạc trong sổ chi tiết. **Việc NÀY (join Module 1
         ↔ Module 3 theo lô) CHƯA code** — gộp chung vào việc viết lại
         `parse_sheet()` bên dưới (cùng 1 lần sửa, vì cả 2 đều cần dò
         đúng cấu trúc nhiều-dòng-1-giao-dịch của file trạm thật).
      - **Đã sửa ngay được** (độc lập, rủi ro thấp):
        `import_hang_nhap_luong2.py` thiếu đọc đúng 8 cột cuối
        (`VCBX`/`Cân than`/`Vun gon`/`AK`/`V`/`W`/`Q`/`S`) dù model đã
        có sẵn field — khảo sát trước chỉ dừng ở cột `KC`. Đã bổ sung
        `ANH_XA_COT`, kiểm chứng đúng bằng chính lô GOLDEN STAR trên.
        Test: `tests/test_import_hang_nhap_luong2.py::test_doc_sheet_doc_dung_8_cot_con_thieu_truoc_do`.
- [x] **3 lỗi thật mới, phát hiện khi dry-run `import_from_excel.py`
      với file trạm thật `NXT Tân Đức 5.xlsx` (2026-07-08)** — sửa
      xong:
      5. `_tim_header_meta()`: nhãn "Tên vật tư:" trong file thật LUÔN
         RỖNG (giá trị thật nằm ở nhãn khác "Danh điểm vật tư : X" —
         1 chuỗi duy nhất, không tách ô) — trước đây `meta.get("ten_sp",
         ws.title)` không fallback được vì key vẫn tồn tại (chỉ rỗng),
         khiến MỌI sheet nhập với `ten_sp=""`. Sửa: ưu tiên tách chuỗi
         "Danh điểm vật tư", chỉ dùng "Tên vật tư" khi có giá trị thật.
      6. `_tim_dong_header()`/`parse_sheet()`: file trạm thật có CẢ
         sheet không phải "Sổ chi tiết vật tư" (sheet tổng hợp "NXT",
         danh sách tra cứu...) xen giữa — trước đây `raise ValueError`
         làm crash cả file. Sửa: trả về `None`, `import_file()` bỏ qua
         nhẹ nhàng (ghi `"bỏ qua"` vào tổng kết, không phải lỗi).
      7. `_tim_loai_giao_dich()`: **luôn** trả về mặc định
         `nhap_mua`/`xuat_ban`, không hề đọc `Diễn giải` — nghĩa là 14
         loại chi tiết (`nhap_che_bien`, `xuat_pha_tron`...) chưa từng
         được phân loại đúng trong toàn bộ dữ liệu import trước đó. Sửa:
         so khớp `Diễn giải` (đã chuẩn hoá) với `LoaiGiaoDich.ten` —
         dữ liệu thật cho thấy `Diễn giải` ghi gần như ĐÚNG HỆT tên loại
         (vd "Xuất pha trộn"), khớp tốt trong thực tế.
- [x] **VIẾT LẠI HOÀN TOÀN `parse_sheet()`/`_doc_khoi()`/`ghi_vao_db()`
      (2026-07-08)** — quy mô tương đương lần viết lại
      `import_hang_nhap_luong2.py`, giải quyết đủ các điểm còn treo ở
      trên:
      - **Nhiều khối "SỔ CHI TIẾT VẬT TƯ" trong 1 sheet**:
        `_tim_tat_ca_dong_header()` tìm TẤT CẢ dòng header (không chỉ
        dòng đầu), `_doc_khoi()` đọc riêng từng khoảng
        `[header+2, header_kế_tiếp-1]`.
      - **Vị trí cột biến động** (đã đo trên ~1700 sheet: cột "TK đối
        ứng" nằm ở vị trí 7/8/10/11 tuỳ sheet, "Diễn giải" thì ổn định
        cột D trên 1647/1656 sheet): `_resolve_cot()` dò cột bằng NỘI
        DUNG 2 dòng header (dòng nhóm + dòng nhãn con
        "N"/"X"/"Lượng"/"Số tiền"), forward-fill nhãn nhóm cho các cột
        để trống do merge.
      - **44% sheet thật (222/503) chứa NHIỀU HƠN 1 "Danh điểm vật tư"
        khác nhau trong CÙNG 1 sheet** (phát hiện MỚI lúc viết lại,
        không nằm trong danh sách ban đầu) — `parse_sheet()` giờ trả về
        **`list[KetQuaImportSheet]`** (đổi API — xem
        `tests/test_import.py`, giờ phải `[0]`), mỗi khối tự dò tên sản
        phẩm riêng qua `_tim_header_meta(ws, dong_gioi_han=...)` (chỉ
        quét 8 dòng NGAY TRƯỚC khối đó, không quét cả sheet), gộp các
        khối CÙNG tên lại, tách riêng khối khác tên.
      - **Sheet ẩn (`ws.sheet_state != 'visible'`) VẪN đọc bình thường**
        — đã kiểm chứng: sheet ẩn (lô hàng đã hết phát sinh, ẩn cho
        gọn — KHÔNG phải xoá) vẫn có giao dịch thật khác 0. Không lọc
        theo `sheet_state` (mặc định `wb.sheetnames`/`wb[name]` của
        openpyxl vốn đã bao gồm cả sheet ẩn, không cần code thêm).
      - **1 giao dịch Nhập trải nhiều dòng**: dòng đầu (có Ngày) là
        giao dịch CHÍNH; các dòng sau (Ngày rỗng, không Lượng, có Số
        tiền) là phụ phí — gắn vào giao dịch CHÍNH gần nhất **THEO VỊ
        TRÍ đọc trong cùng khối** (`cha_so_dong_excel`), thay hẳn cách
        đoán "gần nhất cùng ngày" cũ (đã chứng minh sai qua test
        `test_ghi_vao_db_gan_dung_phu_phi_vao_dung_giao_dich_cung_ngay`
        — 2 giao dịch cùng ngày, thiết kế cũ sẽ gắn nhầm). Nhãn phí lấy
        từ cột "Đơn giá" nếu là text (BH/KC/Cân than/Cồn đống); nếu là
        số thì ghi "Phụ phí chưa rõ tên" + cảnh báo đối chiếu lại với
        `hang_nhap` (chưa tự động join — để dành, xem mục dưới).
      - 2 lỗi thật khác lộ ra khi viết test bằng dữ liệu thật:
        regex tách "Tháng X năm Y" không khớp định dạng thật
        `"Tháng M/YYYY"` (luôn ra `nam=None`, làm sai `ton_dau_ky_dau_tien`
        — lỗi này tồn tại từ code CŨ, chưa từng bị test bắt); dòng tiêu
        đề ("SỔ CHI TIẾT VẬT TƯ"...) của khối SAU bị đọc lẫn vào cuối
        khối TRƯỚC (cột Ngày có chữ → tưởng là giao dịch chính) — loại
        trừ bằng nội dung nhãn tiêu đề, không phụ thuộc ranh giới khối.
      - **Xác nhận với người dùng (2026-07-08) + đã sửa**: cột "Ngày"
        dạng `"N"`/`"N-M"` (vd `"13-13"`) **là "ngày thực hiện" thật**,
        không phải rác — `N` = ngày trong tháng, `N-M` = phiên
        Nhập/Xuất kéo dài từ ngày N đến ngày M (nhiều khi 1 phiên kéo
        dài 2 ngày). **Tháng lấy từ TÊN FILE, năm lấy từ TÊN THƯ MỤC
        cha** (vd `NXT/Tháng 3.2026/NXT Tân Đức 3.xlsx` → tháng=3,
        năm=2026) — KHÔNG dùng tháng/năm mà Excel tự suy đoán khi
        auto-convert chuỗi số nhỏ thành `datetime` (dấu hiệu nhận biết
        lỗi này: ngày==tháng, vd chuỗi `"4-4"` bị Excel tự hiển thị
        thành "4 tháng 4" của 1 năm mặc định nào đó — SAI, vì file thật
        là tháng 3). Hàm mới: `_thang_tu_ten_file()`,
        `_nam_tu_ten_thu_muc()`, `_parse_ngay()` viết lại nhận cả 2
        tham số này. Khi là khoảng 2 ngày, lấy **ngày kết thúc**, kèm
        cảnh báo để đối chiếu lại nếu cần ngày bắt đầu.
      - **Kiểm chứng bằng dữ liệu thật**: dry-run `NXT Tân Đức 3.xlsx`
        (đường dẫn thật, không phải bản sao) — sau khi sửa cột Ngày:
        **0 dòng còn cảnh báo "không đọc được Ngày hợp lệ"** (trước đó
        142 dòng, ~15-20% giao dịch mỗi trạm/tháng), **0 dòng "không
        tìm được giao dịch Nhập cha"** (trước đó 134 dòng — hệ quả dây
        chuyền, giao dịch cha giờ đọc được nên phụ phí gắn đúng theo
        sau). Đối chiếu lại sản phẩm "Cám 5a.1" với sheet "NXT" (tổng
        hợp có sẵn trong chính file Excel, Power Query tính sẵn) —
        **vẫn khớp tuyệt đối** tồn đầu kỳ (6362.63) và tổng nhập lượng
        (12059.67) sau khi sửa, không bị lệch.
      - Test: `tests/test_import_khoi_nhieu_san_pham.py` (9 test — gộp
        nhiều khối cùng sản phẩm, tách 2 sản phẩm khác nhau trong 1
        sheet, gắn phụ phí theo vị trí không đoán ngày, kiểm chứng qua
        `ghi_vao_db()` đầu-cuối, không tạo phụ phí ảo khi Lượng/Tiền
        đều 0, nhận diện mẫu "N"/"N-M" + ưu tiên tháng/năm từ đường
        dẫn, `import_file()` tự suy tháng/năm từ đường dẫn thật), cộng
        `tests/test_import.py` (2 test cũ, đã cập nhật API
        `parse_sheet()` trả `list`).
      - **CÒN TREO thật** (không blocking, ghi để làm sau): join
        `parse_sheet()` ↔ `hang_nhap` (theo trạm + số HĐ/phương tiện)
        để đặt tên chính xác cho "Phụ phí chưa rõ tên" — hiện vẫn đúng
        SỐ TIỀN (gắn đúng giao dịch cha), chỉ chưa chắc đúng TÊN khoản
        phí khi cột Đơn giá là số (không phải text BH/KC/...).

---

## Phase 1 — Module 2: ngân hàng tên than (đầy đủ)

Mở rộng phần lõi đã có ở 0.3 thành 1 module quản lý thật sự, vì đây
là nơi mọi module sau tra cứu để chuẩn hoá tên than.

- [x] Màn hình quản lý danh mục `san_pham` + `san_pham_alias` (CRUD)
      — `frontend/ten-than.html`, API `/api/danh-muc/san-pham-alias`
- [x] Màn hình duyệt "tên than chưa nhận diện" — cùng trang, gọi
      `/api/danh-muc/ten-than-cho-duyet/{id}/gan-alias` hoặc `.../tao-moi`
      (2 endpoint mới trong `danh_muc.py`, có test API end-to-end)
- [x] **Xong (2026-07-08)** — `import_excel/seed_ten_cam.py`: đọc sheet
      `Tên cám` (`Tổng hợp NXT các trạm <năm>.xlsx`), TẠO THẲNG
      `san_pham` cho mỗi tên duy nhất (khác luồng import giao dịch
      thường: đây là dữ liệu KHỞI TẠO ngân hàng tên, không vi phạm yêu
      cầu #5 — xem docstring script). Cột "Biểu 7"/"Biểu 8"/"Tên TD"
      KHÔNG lưu vào `san_pham_alias` (không phải tên tra cứu đầu vào,
      chỉ là nhãn gộp nhóm báo cáo) mà lưu vào 3 field MỚI trên
      `SanPham`: `nhom_bm7`/`nhom_bm8`/`nhom_bmtd` + `co_tu_doanh`
      (bool, cờ `TD`) — xem `app/models.py`, 2 file `schema/*.sql`.
      Idempotent (chạy lại an toàn, chỉ cập nhật nếu đổi). **Áp dụng
      thật vào DB dev**: đọc 272 dòng → tạo 223 `san_pham` (49 dòng
      trùng sau chuẩn hoá khoảng trắng tự gộp). Test:
      `tests/test_seed_ten_cam.py` (5 test, có kiểm chứng số liệu thật
      272→223 qua dry-run trước khi ghi thật).
      Named range `Cam_B8` (`THP.Biểu mẫu Quyết toán KVCP 2026.xlsx`,
      dùng cho Module 8 cân bằng chất lượng) — **CHƯA làm**, để dành
      khi bắt đầu Module 8, xem `md/01-...md` mục 3.
- [x] **Chuẩn hoá tên mạnh hơn + gợi ý fuzzy-match — xong (2026-07-09)**,
      theo đúng yêu cầu người dùng "sheet Tên cám hàng tháng có tên
      than mới chưa chuẩn hoá — TH1 là than cũ viết sai (dấu cách, ký
      tự đặc biệt, phải TỰ nhận biết), TH2 là than mới thật (thêm vào
      cuối danh sách, người dùng tự chuẩn hoá tay)":
      - TH1: `app/services/ten_than.py::chuan_hoa()` nay quy đổi thêm
        non-breaking space + các biến thể dấu gạch ngang (en-dash,
        hyphen đặc biệt...) về 1 dạng chuẩn; `tim_san_pham()` nay so
        khớp qua `_khoa_so_khop()` (chuẩn hoá + hạ chữ thường) —
        **không phân biệt hoa/thường** (đúng như tài liệu CLAUDE.md
        mục 3 đã ghi từ trước nhưng code CŨ chưa thực sự làm — lỗi cũ,
        đã sửa). `import_excel/seed_ten_cam.py` gộp dùng CHUNG
        `chuan_hoa()` này (trước đó tự định nghĩa riêng, dễ lệch).
      - TH2: `goi_y_san_pham_gan_giong()` (dùng `difflib`, không thêm
        thư viện ngoài) tính điểm giống nhau với các `san_pham` đã có,
        trả về endpoint `GET /api/danh-muc/ten-than-cho-duyet` (field
        `goi_y` mới) — `frontend/ten-than.html` hiển thị gợi ý ngay
        trong từng dòng "hàng đợi chờ duyệt", bấm 1 nút để điền sẵn
        dropdown "gán vào sản phẩm đã có" (vẫn cần người dùng bấm xác
        nhận — không tự động gán, tránh gộp nhầm 2 than thật sự khác
        nhau).
      - Test: `tests/test_ten_than.py` (10 test — chuẩn hoá, so khớp
        không phân biệt hoa/thường + dấu gạch ngang, gợi ý đúng/không
        gợi ý khi quá khác, API kèm gợi ý).
- [x] **Reset đầu năm cho than nhập khẩu — xong (2026-07-09)**, theo
      đúng yêu cầu người dùng (giống hành vi sheet `Tên cám` gốc): than
      **trong nước** (vd "Cám 4b.1 BT (tự doanh)") kế thừa nguyên qua
      các năm; than **nhập khẩu** mỗi năm chỉ giữ lại sản phẩm CÒN TỒN.
      - Thêm field `san_pham.nguon_goc` (`trong_nuoc`/`nhap_khau`/NULL
        = chưa phân loại) — **ĐỘC LẬP với `co_tu_doanh`** (xác nhận
        với người dùng: 2 khái niệm khác nhau, không suy ra được từ
        nhau). Model `app/models.py::NguonGocThan`, DDL cả 2
        `schema/*.sql`. DB dev SQLite cũ (tạo trước khi có cột này)
        được tự động `ALTER TABLE ADD COLUMN` khi khởi động
        (`app/database.py::_them_cot_thieu_sqlite()` — chưa có
        Alembic, đây là giải pháp tạm cho SQLite dev, KHÔNG áp dụng
        Postgres).
      - `app/services/ten_than.py::reset_nam_moi_than_nhap_khau(db,
        nam_cu)` — HÀNH ĐỘNG TƯỜNG MINH (giống "chốt kỳ" Module 6,
        KHÔNG tự chạy ngầm): với mọi `san_pham.nguon_goc=nhap_khau`
        đang active, tính tổng tồn cuối THÁNG 12/`nam_cu` (cộng qua
        mọi trạm, dùng lại `ton_kho.py::ton_cuoi_ky()`), nếu ≤0 thì
        đặt `active=False` (ẩn, KHÔNG xoá cứng — đúng nguyên tắc #4).
        API `POST /api/danh-muc/san-pham/reset-nam-moi?nam_cu=`.
        `frontend/ten-than.html`: dropdown "Nguồn gốc" khi thêm sản
        phẩm + cột hiển thị trong bảng danh mục + nút "Reset than nhập
        khẩu hết tồn" (nhập năm cũ, xác nhận trước khi chạy).
      - Test: `tests/test_ten_than.py` (4 test — ẩn đúng khi hết tồn,
        giữ khi còn tồn, không đụng than trong nước, API end-to-end).

---

## Phase 2 — Module 3: hàng nhập ✅ (2026-07-08, hoàn tất đầy đủ)

Thiết kế 2 luồng — xem `CLAUDE.md` mục 5 phần "Module 3". Vùng nháp là
**bảng staging riêng trong CSDL** (`hang_nhap_draft`), không phải file
tạm trên đĩa. **Công thức ĐN QÂ đã xác nhận** bằng 2 file thật độc lập
(khớp đến từng đồng) — không còn là ẩn số:
```
hao_hut = luong_CNchuaQA − ĐN_QÂ    hao_hut_qa = ĐN_QÂ − luong_HD
```

- [x] Schema: `app/models_hang_nhap.py` — `HangNhapDraft`/`HangNhap`,
      `dn_qa` sửa lại đúng kiểu khối lượng (Numeric 18,3, không phải
      Numeric 9,4 dạng % như ước lượng ban đầu).
- [x] `app/services/hang_nhap.py`: `them_dong_luong_1()`,
      `them_dong_luong_2()`, `chot_draft()`, `tinh_hao_hut_tu_dn_qa()`
      (hàm thuần áp dụng công thức đã xác nhận). `chot_draft()` giờ
      **chỉ cần `dn_qa`** — hao_hut/hao_hut_qa **tự động tính**, không
      còn bắt nhập tay 2 giá trị như thiết kế ban đầu.
- [x] `app/routers/hang_nhap.py` + `app/schemas_hang_nhap.py`:
      `ChotDraftIn` bỏ field `hao_hut_qa` (không còn cần truyền vào).
- Luồng 1 (từ file BKHN gốc, than nhập khẩu — cần ĐN QÂ):
  - [x] `import_excel/import_hang_nhap_luong1.py::import_folder()` —
        quét thư mục file BKHN rời rạc, port logic định vị ô của
        `bkhn_td_gui.py`. **Kiểm chứng bằng 97 file thật** (dry-run,
        `HÀNG NHẬP\T5\HÀNG NHẬP T5.26`) — 0 lỗi.
  - [x] **Mới thêm**: `import_file_da_gop()` (`--da-gop`) — đọc thẳng
        1 file ĐÃ GỘP (đầu ra thật của `bkhn_td_gui.py`, có thể đã
        điền tay cột "ĐN QÂ"), dò cột theo TÊN (không theo vị trí, vì
        cột chèn tay lệch vị trí giữa các file). **Kiểm chứng end-to-
        end với file thật** `HÀNG NHẬP T5.26-KD THAN TÂN ĐỨC.xlsx` —
        kết quả `hao_hut`/`hao_hut_qa` tính ra khớp chính xác dữ liệu
        thật (dn_qa=1954.9 → hao_hut=-5.76, hao_hut_qa=73.8).
  - [x] Nháp khi thiếu `ĐN QÂ`, chốt tự tính hao_hut/hao_hut_qa — có
        test (`tests/test_hang_nhap.py`, `tests/test_import_hang_nhap_luong1.py`).
  - [x] Tổng quát hoá cho các trạm khác ngoài Tân Đức — **đã xác nhận
        (2026-07-08): KHÔNG cần**. Các trạm khác gửi dữ liệu về đúng
        format `Hàng nhập <năm>.xlsx` (luồng 2), luồng 1 chỉ là tool
        hỗ trợ riêng cho Tân Đức.
  - [ ] "Phí kẹp" nhánh cũ trong `bkhn_td_gui.py` (hao_hut_qa=0 giả)
        không còn quan trọng nữa vì `chot_draft()`/`them_dong_luong_1()`
        giờ **luôn ghi đè** bằng công thức đã xác nhận khi có `dn_qa`
        — nhánh nào cũng cho kết quả đúng sau khi chốt.
- [x] Luồng 2 (file "Hàng nhập <năm>.xlsx" đã gộp sẵn — ghi thẳng,
      không qua nháp, **đã xác nhận lý do**: cột đã khớp CSDL, thiếu
      ĐN QÂ ở nhiều dòng là ĐÚNG vì than nội địa/phiếu điều chỉnh giá
      không cần ĐN QÂ, không phải thiếu sót):
      `import_excel/import_hang_nhap_luong2.py` — **viết lại hoàn
      toàn** sau khi phát hiện khảo sát ban đầu SAI (xem `md/01-...md`
      mục 5c): thật ra có **nhiều sheet T1..T12** (bỏ qua biến thể
      `(DD)` = lô đang đi đường chưa về kho), **header ở dòng 3**
      (không phải dòng 1), cột `HH`/`HHQA` đã tính sẵn trong file
      (lấy trực tiếp, không tính lại). **Kiểm chứng bằng file thật**
      — đọc đúng 1312 dòng qua sheet T1-T5, bỏ đúng sheet `(DD)`.
- [x] Frontend: `frontend/hang-nhap.html` — cập nhật bỏ cột "Hao hụt
      QÂ" (giờ tự tính), chỉ còn nhập "ĐN QÂ" rồi Chốt.
- [x] Test: `tests/test_hang_nhap.py` (7 test), `tests/test_import_hang_nhap_luong1.py`
      (3 test, kể cả kiểm chứng file thật), `tests/test_import_hang_nhap_luong2.py`
      (5 test, layout thật nhiều sheet + bỏ qua `(DD)`).

---

## Phase 3 — Module 4: phương án phối trộn (PA) ✅

Nguồn: `Sổ theo dõi PA trạm 2026.xlsx` (sheet T1..T12). **Vị trí cột đã
xác minh bằng dữ liệu thật** (không phải suy đoán từ M code) — xem
docstring `import_excel/import_phuong_an.py`.

- [x] Schema: `app/models_phuong_an.py` — bảng `phuong_an` (SPT, ngày
      HĐ/PT/NT, trạm, than đầu ra + than đầu vào — **cả 2 tên than
      đều qua gate riêng**, Ak/Vk/Sk/Qk, L_100/L_NT, cờ Cảng). DDL đã
      thêm vào `schema_sqlite.sql`/`schema_postgres.sql`.
- [x] `app/services/phuong_an.py::them_dong()` — 1 dòng PA bị chặn
      nếu than đầu ra HOẶC than đầu vào chưa nhận diện được (báo rõ
      cái nào), có test.
- [x] `import_excel/import_phuong_an.py` — đọc đúng layout thật
      (KHÔNG có dòng header, đọc theo vị trí cột + điều kiện lọc gốc
      của Power Query `Cột29=2, Cột28 rỗng, Cột7 khác rỗng` để chỉ
      lấy dòng dữ liệu thật, bỏ qua dòng nháp/lỗi công thức
      `#DIV/0!`). Đã dry-run với file thật `Sổ theo dõi PA trạm
      2026.xlsx` — xử lý đúng 2322 dòng qua cả 12 sheet T1-T12, 0 lỗi.
- [x] `app/routers/phuong_an.py` — API chỉ đọc (nhập liệu qua import
      script, không có màn hình nhập tay — dữ liệu luôn từ Excel).
- [x] Frontend: `frontend/phuong-an.html` — xem danh sách PA, lọc theo
      trạm/năm/tháng/SPT, nhóm hiển thị theo SPT.
- [x] Test: `tests/test_phuong_an.py` (4 test — gate chặn đúng khi 1
      trong 2 tên than lạ, đọc đúng vị trí cột + điều kiện lọc, import
      qua gate end-to-end).
- [x] Công thức `L_B` (lượng bán) trong QTTPT — **đã xác nhận đầy đủ
      (2026-07-08)**: `L_TT`=tồn đầu kỳ, `L_TTN`=tồn cuối kỳ,
      `L_HHB`=hao hụt bán; công thức là 1 cân đối kho chuẩn, xem
      `CLAUDE.md` mục "việc chưa xác nhận" + `md/01-...md` mục 4.
      Sẵn sàng dùng làm căn cứ cho Module 7 (QTTPT).

---

## Phase 4 — Module 5: tổng hợp liên trạm ✅ (2026-07-08, phần service/API/frontend xong)

- [x] `app/services/tong_hop.py::tong_hop_lien_tram()` — gộp NXT theo
      (trạm, chủng loại) cho 1 kỳ, tính TRỰC TIẾP từ `giao_dich_kho` đã
      có qua Module 1 (không đọc lại Excel) — thay cho Power Query gộp
      `Tổng hợp NXT các trạm <năm>.xlsx`. Khác
      `ton_kho.py::tong_nhap_xuat_thang()` (chỉ gộp theo nhóm Nhập/Xuất):
      ở đây gộp chi tiết theo **từng loại trong 14 loại**
      (`nhap_mua`/`nhap_che_bien`/.../`xuat_pha_tron`/`xuat_khac`...)
      đúng layout BM7. Mỗi dòng kèm `nhom_bm7`/`nhom_bm8`/`nhom_bmtd`
      lấy từ `san_pham` (đã có nhờ `seed_ten_cam.py` — xem Phase 1) để
      Module 9 gộp nhóm báo cáo sau này. Chỉ trả dòng có dữ liệu (tồn
      đầu ≠ 0 hoặc có giao dịch trong kỳ).
- [x] `app/routers/tong_hop.py` — `GET /api/tong-hop/nxt-lien-tram?nam=&thang=&ma_tram=`
      (chỉ đọc, không có nhập tay — dữ liệu từ Module 1).
- [x] Frontend: `frontend/tong-hop.html` — bảng NXT theo trạm/chủng
      loại, đủ cột chi tiết Nhập/Xuất theo BM7, lọc theo trạm/năm/tháng.
- [x] Test: `tests/test_tong_hop.py` (4 test — gộp đúng nhiều loại giao
      dịch, gộp nhiều trạm + lọc theo mã trạm, bỏ qua cặp không có dữ
      liệu, API end-to-end).
- [ ] **CHẶN bởi lỗi Module 1** (xem Phase 0.4 "còn treo"): chưa thể
      test Module 5 với dữ liệu THẬT nhiều trạm vì
      `import_from_excel.py` chưa đọc đúng file trạm thật nhiều tháng
      — hiện chỉ kiểm chứng bằng dữ liệu tự tạo trong test. Cần sửa
      xong parser Module 1 trước khi coi Module 5 là "đã kiểm chứng
      bằng dữ liệu thật" như các module trước.
- [ ] Đầu ra đúng layout cần cho Module 9 (BM7/BM8) — đã có field
      `nhom_bm7`/`nhom_bm8` sẵn sàng, nhưng bước GỘP THEO NHÓM (rollup
      nhiều `san_pham` cùng 1 nhóm thành 1 dòng báo cáo) chưa làm —
      để dành cho Module 9.

---

## Phase 5 — Module 6: phân bổ Tồn/HHB/HHKK theo lô ✅ (2026-07-09, xong phần lõi)

Thuật toán waterfall đã xác nhận — xem `CLAUDE.md` nguyên tắc #2 +
`md/01-...md` mục 8.

- [x] Schema: `app/models_phan_bo.py` — `KetQuaKiemKe` (nhập tay Tồn
      cuối thực tế/HHKK/HHB/XCN/NCN theo kỳ), `PhanBoSnapshot` (1 dòng
      = 1 lần tính cho 1 kỳ, cờ `da_chot`), `PhanBoChiTiet` (kết quả
      phân bổ xuống từng `PhuongAn`, tách theo `ton`/`hhkk`/`hhb`). DDL
      thêm vào cả `schema_sqlite.sql`/`schema_postgres.sql`.
- [x] Màn hình nhập tay kết quả kiểm kê thực tế (Tồn, HHKK) theo
      (trạm, sản phẩm, tháng) — `frontend/phan-bo.html`, API
      `POST/GET /api/phan-bo/kiem-ke`. Có thêm HHB/XCN/NCN (mặc định
      0) để người dùng có chỗ ghi giá trị cuối cùng, kèm nút "gợi ý"
      HHB (xem mục dưới).
- [x] Thuật toán phân bổ: `app/services/phan_bo.py::phan_bo_waterfall()`
      (hàm THUẦN, không đụng DB) — Tồn → PA gần nhất; HHKK → PA gần
      nhất theo ngày kiểm kê; HHB → phần PA còn lại, gần nhất lùi về
      trước. "Gần nhất" đo bằng `ngay_nt` (ưu tiên) → `ngay_pt` →
      `ngay_hd` của PA. Mỗi PA có "sức chứa" = `l_nt` trừ đi phần ĐÃ
      phân bổ ở CÁC KỲ KHÁC trước đó (query qua `phan_bo_chi_tiet` join
      `phan_bo_snapshot`) — cho phép 1 lô dùng dần qua nhiều tháng liên
      tiếp, đúng tinh thần luỹ kế của sheet `Append1`/`LK` gốc. Test
      hồi quy riêng cho trường hợp này:
      `test_phan_bo.py::test_tinh_phan_bo_ky_sau_tru_dung_suc_chua_da_dung_o_ky_truoc`.
- [x] Action "tính lại phân bổ" tường minh
      (`app/services/phan_bo.py::tinh_phan_bo()`, API
      `POST /api/phan-bo/tinh`) cho kỳ chưa chốt; khoá cứng
      (`ValueError` → HTTP 400) không tự tính lại cho kỳ đã chốt
      (`chot_ky()`/`POST /{id}/chot`) — phải gọi `mo_lai_ky()`/
      `POST /{id}/mo-lai` mới sửa được. Test:
      `test_phan_bo.py::test_chot_ky_khoa_khong_cho_tinh_lai`.
- [x] Đối chiếu tổng phân bổ ra với tổng đầu vào (giống sheet
      `Check`/`CheckKQ` trong `Tính tồn 2.xlsx`): `PhanBoSnapshot` lưu
      `ton_chua_phan_bo`/`hhkk_chua_phan_bo`/`hhb_chua_phan_bo` (>0
      nghĩa là dữ liệu PA không đủ để giải thích hết số kiểm kê, cần
      rà soát) + trả về `canh_bao` dạng text từ API. Test:
      `test_phan_bo.py::test_tinh_phan_bo_khong_du_pa_bao_canh_bao`.
- [x] Test: `tests/test_phan_bo.py` (11 test — 5 test hàm thuần
      waterfall/công thức cân đối, 5 test service DB thật (end-to-end,
      cảnh báo thiếu dữ liệu, lỗi khi chưa có kiểm kê, khoá/mở kỳ, luỹ
      kế qua nhiều kỳ), 1 test API end-to-end qua `TestClient`).
      `pytest tests/ -v`: 62/62 xanh. Smoke test qua `uvicorn` thật
      bằng `curl` (không chỉ `TestClient`) — xem ghi chú "Trạng thái
      tổng quan" phía trên.
- [x] **Đã xác nhận nguồn thật (2026-07-09)** — xem
      `md/power_query/QTTPT_2026.m` dòng 165-197 + `CLAUDE.md` mục 6:
      `L_XCN`/`L_NCN` KHÔNG map vào 14 mã `loai_giao_dich` của Module 1
      — cả 2 đọc từ CÙNG 1 sheet `CN` trong `QTTPT 2026.xlsx` (Module
      7, chưa xây), dữ liệu THEO TỪNG LÔ/PA (không phải tổng theo kỳ
      như Tồn/HHKK/HHB). **Việc đọc sheet `CN` này thuộc phạm vi Module
      7** (xem Phase 6 dưới) — Module 6 KHÔNG cần tự làm, thiết kế hiện
      tại (`KetQuaKiemKe.xcn`/`.ncn` nhập tay, mặc định 0) là bước đệm
      tạm ĐÚNG cho tới khi Module 7 có dữ liệu `CN` thật. Khi đó
      `app/services/phan_bo.py::goi_y_hhb()` nên đổi nguồn xcn/ncn từ
      nhập tay sang SUM theo (trạm, sản phẩm, tháng) từ các dòng `CN`
      liên quan — giống cách `l_pa` hiện SUM từ `PhuongAn`. Không phải
      việc treo của Module 6 nữa, chuyển ghi chú sang Phase 6.
- [ ] Chưa kiểm chứng bằng dữ liệu THẬT (khác các module trước) — mới
      test bằng dữ liệu tự tạo (unit test + smoke `curl`). Cần đối
      chiếu lại với 1 kỳ thật trong `Tính tồn 2.xlsx` (sheet
      `Check`/`CheckKQ`) khi có số liệu, đặc biệt để xác nhận đúng ý
      nghĩa "sức chứa luỹ kế qua nhiều tháng" của PA khớp với cách file
      Excel gốc tính `Append1`/`LK`.
- [ ] Frontend `phan-bo.html` mới smoke-test qua `curl`/API, CHƯA tự
      thao tác qua trình duyệt thật (chọn dropdown, bấm nút, xem bảng
      kết quả) — nên làm trước khi giao người dùng thật sử dụng.

---

## Phase 6 — Module 7: quyết toán than pha trộn (QTTPT) 🔶 mới có 1 phần (2026-07-09)

- [x] **Tính lượng bán (L_B) theo từng lô — xong (2026-07-09)**:
      `app/services/quyet_toan.py::tinh_luong_ban_theo_lo()`, API
      `GET /api/quyet-toan/luong-ban`, `frontend/quyet-toan.html`.
      Thay thế query `Bán`/`tenthan` trong
      `md/power_query/QTTPT_2026.m` dòng 140-153: với 1 (tram_san_pham,
      nam, thang), với MỖI lô/PA tính
      `L_B = L_TTT + L_PA − L_HHB − L_KK − L_TTN + L_NCN − L_XCN`
      (đúng công thức cân đối đã xác nhận, áp dụng ở MỨC LÔ thay vì mức
      tổng như `phan_bo.py::tinh_hhb_can_doi()`), lấy trực tiếp từ dữ
      liệu ĐÃ CÓ: `L_TTT`/`L_TTN` = kết quả phân bổ Tồn của Module 6
      (tháng trước/tháng này, CÙNG 1 lô — có test hồi quy xác nhận lấy
      đúng tồn cuối tháng trước làm tồn đầu tháng này), `L_PA` = PA.l_nt
      nếu PA nghiệm thu ĐÚNG tháng đang xét, `L_HHB`/`L_KK` = kết quả
      phân bổ HHB/HHKK của Module 6 tháng này. `L_XCN`/`L_NCN` **luôn
      = 0** (chưa có nguồn — xem mục dưới), đây là giới hạn CHƯA giải
      quyết, không phải lỗi. Test: `tests/test_quyet_toan.py` (4 test —
      2 test service tính đúng công thức bằng tay, tháng đầu/tháng sau
      nối tiếp qua lô, 1 test rỗng, 1 test API). `pytest tests/ -v`:
      66/66 xanh. Smoke-test qua `uvicorn` thật bằng `curl`, số ra khớp
      tính tay.
- [x] **Đã chốt (2026-07-09): "giá vốn than" KHÔNG cần tự động hoá** —
      user xác nhận vẫn tính tay, module không cần làm phần này. Sheet
      `Giá vốn 6b.1`/`Giá vốn than trong nước`/`Quyết toán` trong
      `QTTPT 2026.xlsx` (công thức Excel thuần, không có trong M code)
      giữ nguyên quy trình tính tay hiện tại.
- [x] Xác nhận ý nghĩa đầy đủ `HHB`/`HHKK`/`XCN`/`NCN`/`KVCP`/`QTTPT`
      — xong 2026-07-08, xem `md/01-...md` mục 6: KVCP=Kho vận Cẩm
      Phả, HHB=Hao hụt bán, HHKK=Hao hụt kiểm kê, XCN=Xuất chuyển
      nguồn, NCN=Nhập chuyển nguồn, QTTPT=Quyết toán than pha trộn
      (không phải "tổn phí" như dùng nhầm trước đó)
- [ ] Đầu ra khớp layout `QTTPT 2026.xlsx` (sheet `Quyết toán`...) —
      chưa làm, cần file thật để đối chiếu layout in ấn.
- [ ] **Nguồn XCN/NCN đã xác định (2026-07-09)** — xem `CLAUDE.md` mục
      6 + `md/power_query/QTTPT_2026.m` dòng 165-197: cả 2 đọc từ CÙNG
      1 sheet `CN` trong `QTTPT 2026.xlsx`, dữ liệu THEO TỪNG LÔ/PA
      (giống shape PA: `SPT, N_HD, N_PT, N_NT, Tram, L_100, Ak, Vk, Sk,
      Qk, L_T, STTPA, Cảng, Tháng...`), KHÔNG phải tổng theo kỳ, nhưng
      **CHƯA xây** vì sheet `CN` có thêm các cột
      `C_TP`/`C_PT`/`PL`/`C_B8`/`C_CN` chưa xác nhận ý nghĩa — đoán sai
      sẽ làm sai số liệu kế toán thật, cần file `QTTPT 2026.xlsx` thật
      + hỏi kế toán trước khi code. Sau khi có bảng dữ liệu `CN`, quay
      lại sửa CẢ `app/services/phan_bo.py::goi_y_hhb()` (Module 6) LẪN
      `app/services/quyet_toan.py::tinh_luong_ban_theo_lo()` (Module 7,
      hiện đang hard-code `l_xcn=l_ncn=ZERO`) để SUM đúng từ đó thay vì
      nhập tay/mặc định 0 như hiện tại.

---

## Phase 7 — Module 8: cân bằng chất lượng 🔶 mới có phần lõi (2026-07-09)

- [x] **Bình quân gia quyền Ak/Vk/Sk/Qk theo nhóm Biểu 8 — xong phần
      lõi (2026-07-09)**: `app/services/can_bang_chat.py`, API
      `GET /api/can-bang-chat`, `frontend/can-bang-chat.html`. Gộp tất
      cả `san_pham` cùng `nhom_bm8` tại 1 trạm, tính bình quân gia
      quyền `khoi_luong` cho 3 "trạng thái" (Tồn cuối kỳ theo lô — từ
      Module 6 `loai='ton'`; Nhập trong kỳ theo lô — từ Module 4
      `PhuongAn.l_nt`; Bán trong kỳ theo lô — từ Module 7
      `tinh_luong_ban_theo_lo()`). Hàm thuần
      `binh_quan_gia_quyen()` xử lý đúng trường hợp thiếu 1 chỉ tiêu ở
      1 lô (không tính lô đó vào TRUNG BÌNH của riêng chỉ tiêu thiếu,
      tránh kéo lệch sai) và bỏ qua khối lượng ≤ 0. Test:
      `tests/test_can_bang_chat.py` (7 test — 4 test hàm thuần, 1 test
      end-to-end gộp 2 san_pham cùng nhóm tính tay khớp, 1 test lỗi
      nhóm không tồn tại, 1 test API). `pytest tests/ -v`: 73/73 xanh.
      Smoke-test qua `uvicorn` thật bằng `curl`, số ra khớp tính tay.
- [x] **Đã có file `Cân bằng chất.xlsx` thật để đối chiếu (2026-07-10)**
      — người dùng cung cấp trực tiếp, đọc bằng `openpyxl` + giải
      thích luồng nghiệp vụ. Kết quả đầy đủ ở `md/01-...md` mục 9.
      Tóm tắt: đã xác nhận nguồn `CLB` (từ sheet `BK chứng thư`, khớp
      số tuyệt đối), đã giải mã cột `PL`=TN/NK (`CLAUDE.md` mục 6).
- [ ] **PHÁT HIỆN QUAN TRỌNG (2026-07-10) — thiết kế hiện tại CHƯA đủ,
      không chỉ là "chưa đối chiếu số"**: quy trình thật KHÔNG dừng ở
      bình quân gia quyền đơn thuần. Có thêm 1 bước **hiệu chỉnh chất
      lượng từng cám thành phần cho khớp với `CLB`** (chất lượng bán
      thực đo), thực hiện **THỦ CÔNG theo kinh nghiệm người làm** (xác
      nhận trực tiếp từ người dùng — không phải công thức cố định như
      quy tắc làm tròn phân bổ lượng ở Module 6). Kết quả hiệu chỉnh
      này (không phải bình quân gia quyền gốc) mới là dữ liệu cấp cho
      `DCCL`. Xem `md/01-...md` mục 9c để biết đầy đủ cơ chế (dòng
      chênh lệch, bước 0,01/1 chỉnh tay).
      **Việc cần làm khi code tiếp Module 8**: thêm 1 bước "gợi ý bình
      quân gia quyền + hiển thị chênh lệch với `CLB` + người dùng xác
      nhận/chỉnh tay giá trị cuối" — cùng tính chất với `ĐN QÂ` (Module
      3)/kết quả kiểm kê (Module 6), KHÔNG coi là giá trị suy ra thuần
      tuý như thiết kế hiện tại của `can_bang_chat.py`.
      Còn treo (chưa xác nhận): công thức chính xác cột `B_Ak`/`B_Vk`/
      `B_Qk`/`B_Sk`/`Round` trong sheet `Bán2`; vai trò bảng hệ số ở
      sheet `Tính Q` (nghi ngờ dùng để quy đổi chênh lệch Ak→Qk); vai
      trò sheet `Sheet1`/`PL`/`THmuaKV`.
- [x] `Cân bằng chất.xlsx` là bản CHÍNH THỨC (xác nhận 2026-07-08) —
      đích đối chiếu là sheet `DCCL` trong `THP.Biểu mẫu Quyết toán
      KVCP 2026.xlsx` (không phải `Bieu8 canbangchat` như suy đoán ban
      đầu — xem `md/01-...md` mục 6)
- [x] **Đã đối chiếu `DCCL` bằng file thật, khớp tuyệt đối (2026-07-10)**
      — người dùng cung cấp trực tiếp `QTTPT 2026.xlsx` +
      `THP.Biểu mẫu Quyết toán KVCP 2026.xlsx`. Xem `md/01-...md` mục
      10b. Xác định chính xác: `DCCL` lấy dữ liệu từ khối cột **R-U**
      của sheet `B8` (không phải N-Q) — quan trọng vì `B8` có nhiều
      khối cột hiệu chỉnh liên tiếp, dễ nhầm khối. Đã kiểm chứng 1
      dòng thật khớp tuyệt đối (Lượng/AK/Vk/Qk/Sk).
- [x] **Sheet `CN` — đã tìm thấy bảng thật, giải quyết dứt điểm
      (2026-07-10)**: nằm trong sheet `XCN` của `QTTPT 2026.xlsx`, đủ
      21 cột. Cơ chế: 1 dòng = 1 giao dịch chuyển nguồn, chuyển lượng
      của 1 thành phần từ tính-vào sản phẩm `C_TP` sang tính-vào sản
      phẩm `C_CN`. Xem `md/01-...md` mục 10a + `CLAUDE.md` mục 6. Sẵn
      sàng code Module 7 đọc bảng này (còn thiếu: viết
      `import_excel` cho bảng `CN`, chưa bắt đầu).

---

## Phase 8 — Module 9: biểu mẫu quyết toán tổng

- [x] Đích thật + header đã xác nhận (2026-07-08, xem `md/01-...md`
      mục 6):
  - `BM7` → `Quyết toán\Bao cáo NXT Biểu 07-TMB-print.xlsx` (NXT theo
    danh mục/chủng loại than, toàn công ty). Sheet `LK` (luỹ kế) +
    `T0`..`T12` (từng tháng). **Header từ dòng 4 đến dòng 7.**
  - `BM8` → `Quyết toán\Biểu 08 TMB-print.xlsx` (NXT chi tiết theo
    từng trạm/cửa hàng). Sheet `LK` + `T0`..`T12` + `GOP`. **Header
    dòng 6 và 7.**
  - `BM PT/TD` → `THỐNG KÊ\Báo cáo NXT TD-CB (tháng)-print.xlsx` (mẫu
    Tập đoàn, TD=Tự doanh/PT=Pha trộn). Sheet `TD0`/`PT0`..`TD12`/
    `PT12` + tổng hợp `PT_G`/`TD_G`/`NXT-TD`/`NXT-PT`. **Header dòng
    7 đến 9.**
- [ ] Xuất Excel/PDF đúng layout 3 biểu trên, dữ liệu từ Module 5 + 7
      + 8
- [ ] Đối chiếu số liệu xuất ra với biểu mẫu Excel cũ (chạy song song
      1-2 kỳ trước khi thay hẳn Excel)

---

## Ghi chú khi cập nhật file này

- Không copy lại lý do/kiến trúc từ `CLAUDE.md` vào đây — chỉ liệt kê
  việc cần làm, trạng thái, và link chéo.
- Khi 1 quyết định "chưa chốt"/"cần hỏi người dùng" được trả lời, cập
  nhật **cả 2 nơi**: `CLAUDE.md` (ghi quyết định + lý do) và ở đây
  (bỏ dấu "hỏi lại", chuyển bước đó thành việc code được).
- Nếu phát sinh module/bước ngoài roadmap ban đầu, thêm vào đúng
  Phase liên quan, không tạo file tiến trình thứ 2.
