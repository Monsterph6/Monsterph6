# Hệ sinh thái file Excel kho than — kết quả khảo sát

Tài liệu này ghi lại những gì đã khảo sát được từ các file Excel thật
(sheet, Power Query M code, đường dẫn liên kết) để làm căn cứ xây dựng
`CLAUDE.md`. Không phải nghiệp vụ nào cũng khẳng định chắc 100% — chỗ
nào chỉ là suy đoán từ tên cột/tên sheet sẽ ghi rõ "(suy đoán)".

Công cụ dùng để khảo sát: `openpyxl` (đọc sheet/data), và một script
Python tự viết để giải nén phần `customXml/item1.xml` (chứa
`DataMashup` — dữ liệu Power Query M code dạng UTF-16LE + base64 +
zip lồng zip) ra text M thuần. Các file M gốc đã lưu tại
`md/power_query/`.

## 1. Bức tranh tổng thể — các lớp dữ liệu

```
Lớp 0 — Chứng từ gốc (per sự kiện)
  ├─ NXT\<Tháng X>\NXT <Trạm> <X>.xlsx        1 file/trạm/tháng, 1 sheet/chủng loại than
  │                                            (ĐÃ có Module 1 "kho_than_module" xử lý)
  └─ HÀNG NHẬP\<Tháng>\...\<mã tàu/chuyến>.xlsx 1 file/lô hàng nhập (BKHN, PNK, BB KL, CA,
                                                 NPHH, BBGĐ, BBGN...)

Lớp 1 — Sổ tổng hợp theo tháng/trạm (thủ công hoặc Power Query gộp)
  ├─ Sổ theo dõi PA trạm 2026.xlsx             sheet T1..T12, theo dõi phương án
  │                                            phối trộn (PA) từng trạm, có Ak/Vk/Sk/Qk
  └─ HÀNG NHẬP\Hàng nhập 2026.xlsx             gộp tất cả lô hàng nhập trong năm

Lớp 2 — Tổng hợp liên trạm + ngân hàng tên than
  └─ Tổng hợp NXT các trạm 2026.xlsx
       ├─ sheet "NXT"                          NXT gộp toàn bộ trạm
       └─ sheet "Tên cám"  ⭐ NGÂN HÀNG TÊN THAN chính (xem mục 3)

Lớp 3 — Quyết toán / báo cáo định kỳ (đích cuối, đúng những gì user liệt kê)
  ├─ QTTPT 2026\QTTPT 2026.xlsx                Quyết toán than pha trộn (Bán/Tồn/HHB/HHKK/XCN/NCN) — xác nhận 2026-07-08 (KHÔNG phải "tổn phí" như suy đoán ban đầu)
  ├─ QTTPT 2026\KVCP\Cân bằng chất.xlsx         Cân bằng chất lượng than (Ak/Vk/Sk/Qk bình quân)
  ├─ QTTPT 2026\KVCP\THP.Biểu mẫu Quyết toán KVCP 2026.xlsx  Biểu mẫu quyết toán khu vực
  └─ Quyết toán\Các biểu 2026-M.xlsx           Biểu tổng (BM7, BM8, CBC, TH-PTTD...)

Lớp hạ tầng dùng chung
  └─ 8. Thủy\Path.xlsx                          bảng "raw path -> path tương đối", Power
                                                 Query dùng để tính đường dẫn tuyệt đối tới
                                                 các file khác trên máy hiện tại — vì các
                                                 workbook được đồng bộ qua OneDrive, đường
                                                 dẫn tuyệt đối khác nhau giữa các máy.
```

**Đính chính quan trọng (2026-07-10) — 2 sheet cùng tên "NXT" khác
nhau, đừng nhầm**: file Lớp 0 (`NXT <Trạm> <tháng>.xlsx`, mỗi trạm/
tháng) **cũng có 1 sheet tên "NXT"** bên trong (ngoài các sheet "Sổ
chi tiết vật tư" theo từng chủng loại) — đây **không phải cùng 1 sheet
"NXT" ở Lớp 2** (`Tổng hợp NXT các trạm.xlsx`). Vai trò đã xác nhận
trực tiếp từ người dùng: **sheet "NXT" ở Lớp 0 là bảng tổng hợp DO
CHÍNH KẾ TOÁN TỪNG TRẠM TỰ LẬP** (không phải giá trị suy ra để đối
chiếu) — công việc thật của người dùng (ứng với Module 5) là **gộp
các sheet "NXT" Lớp 0 này lại giữa các trạm**, tương đương việc tạo ra
sheet "NXT" ở Lớp 2. Việc Module 1 hiện tại parse "Sổ chi tiết vật tư"
(không phải sheet "NXT") thành `giao_dich_kho` là 1 nỗ lực **khác**,
chưa được dùng làm nguồn cho việc tổng hợp — nguyên văn xác nhận:
*"sheet NXT trong từng file ấy là tổng hợp của các nhân viên kế toán,
nhiệm vụ của tôi là tổng hợp lại. tôi chưa triển khai đến sổ chi tiết
vật tư để tổng hợp."* Xem `CLAUDE.md` mục 4 + `TASK.md` Phase 4 để
biết đầy đủ ý nghĩa cho kiến trúc Module 5.

Quan trọng: **rất nhiều query M vẫn trỏ tới đường dẫn tuyệt đối đã hỏng**
(vd. `C:\Users\phamh\OneDrive - Cong ty CP Kinh doanh than Mien Bac -
Vinacomin\...`, `C:\Users\User\OneDrive\...`) — máy cũ, không còn tồn
tại trên máy hiện tại. Đây là bằng chứng cụ thể cho lý do cần bỏ mô
hình "Excel nối Excel qua đường dẫn tuyệt đối" và chuyển sang CSDL
trung tâm.

## 2. Danh sách sheet đã thấy trong 4 file quyết toán tham khảo

| File | Sheet đáng chú ý |
|---|---|
| `Quyết toán\Các biểu 2026-M.xlsx` | Checkthan, CBC (Cân bằng chất?), CheckT, **BM8**, **BM7**, TH-PTTD, BM-PT, BM-TD, DD, Mua, LastBM7, LastBM8, Tên cám, Tên cám (2), NXT than tự doanh, NXT than PTCB |
| `QTTPT 2026\QTTPT 2026.xlsx` | Than, tenthan, Bán, Check, **PA**, Tồn, **HHB**, **HHKK**, T_NK, XCN, T-TN, Quyết toán, Quyết toán (T), Giá vốn than trong nước, Than QN, GV than NK, CÁM 6B.1(BOT..., Cước VC, GIÁM ĐỊNH+THUÊ BÃI, PL, ThanPT, DC, ThanTP |
| `QTTPT 2026\KVCP\THP.Biểu mẫu Quyết toán KVCP 2026.xlsx` | Bieu 1 than KVCP, B2KVCP, B2CNQN, TH 5a.14, Bieu35a10/45a14 (ĐTB/ĐHP/ĐVA), Bieu76b1 (bán), **Bieu8 canbangchat**, B8_NT, xpttk, Bán, Tồn, DCCL, Ton_dau, BSthan, B8_Tồn, Tontram |
| `QTTPT 2026\KVCP\Cân bằng chất.xlsx` | PA, B8 (PA), Tính Q, Bán2, CLB, B8, PL, THmuaKV. **Xác nhận (2026-07-08): đây là file CHÍNH THỨC**, kết quả tính ra phục vụ trực tiếp cho sheet **`DCCL`** trong `THP.Biểu mẫu Quyết toán KVCP 2026.xlsx` (không phải `Bieu8 canbangchat` như suy đoán ban đầu — 2 sheet khác nhau trong cùng file THP) |

Các sheet dạng `Sheet1/Sheet2/Sheet3/Sheet4` không có ý nghĩa nghiệp
vụ — thường là vùng nháp hoặc bảng tham số cho Power Query
(`Excel.CurrentWorkbook(){[Name="..."]}`).

## 3. Ngân hàng tên than (yêu cầu #5 của user)

Đã tìm thấy **không chỉ 1 mà nhiều bảng ánh xạ tên than nằm rải rác**:

1. **`Tổng hợp NXT các trạm 2026.xlsx` → sheet "Tên cám"** — bảng ánh xạ
   chính, 5 cột:
   `Than tại NXT | Biểu 8 | Biểu 7 | TD | Tên TD`
   - `Than tại NXT`: tên như ghi trong sổ NXT trạm (vd. `Cám 5a.1 `,
     `Cám 5a.1 (ĐHP)`, `Cám 4b.1 BT (tự doanh)` — **có cả biến thể
     thừa khoảng trắng, viết tắt trạm, hậu tố "(tự doanh)"**).
   - `Biểu 8` / `Biểu 7`: tên hiển thị chuẩn hoá dùng trong 2 biểu báo
     cáo bắt buộc (BM7, BM8) — nhóm theo khoảng độ tro Ak (vd. "Cám
     5a.10, AK≤31%").
   - `TD`: cờ đánh dấu "tự doanh" (than tự doanh khác than PT/CB —
     phân biệt vì hạch toán khác nhau).
   - `Tên TD`: tên hiển thị khi là than tự doanh.
2. **`THP.Biểu mẫu Quyết toán KVCP 2026.xlsx` → sheet nội bộ "Cam"**
   (query `Cam`, đọc từ `Cam_B8` — 1 named range 2 cột `Cam_all |
   B8`) — một ánh xạ **khác**, tên-than-tại-trạm → tên Biểu 8, dùng
   riêng cho tính "Cân bằng chất" (bình quân gia quyền Ak/Vk/Sk/Qk).
   Query `Toncuoi`/`Toncuoi (3)` gộp file "tồn cuối kỳ" của từng trạm
   (đọc từ 1 thư mục, mỗi trạm 1 file) rồi join với bảng `Cam` này;
   dòng nào **không khớp được** (`Cam.Cam_B8 = null`) bị tách riêng ra
   `Toncuoi (3)` — **đây chính là cơ chế dò tên than lạ hiện tại**,
   nhưng chỉ để lọc âm thầm chứ không cảnh báo chủ động cho người
   dùng.

→ **Kết luận thiết kế**: hệ thống mới cần **một bảng danh mục than
(`san_pham`) làm nguồn sự thật duy nhất**, có thêm bảng **alias**
(tên biến thể / tên viết tắt tại từng trạm / tên hiển thị theo từng
biểu mẫu) trỏ về đúng 1 `san_pham_id`. Không lặp lại việc mỗi workbook
tự có 1 bảng ánh xạ riêng như Excel hiện tại.

## 4. Sổ theo dõi PA trạm — cấu trúc cột

Sheet `T1`..`T12` (mỗi tháng 1 sheet, layout giống hệt nhau), các cột
chính (đã suy ra qua Power Query rename):

| Cột thô | Tên sau rename | Ý nghĩa (suy đoán) |
|---|---|---|
| Column1 | SPT | Số phương án |
| Column2 | N_HD | Ngày hợp đồng/kế hoạch |
| Column3 | N_PT | Ngày phối trộn |
| Column4 | N_NT | Ngày nghiệm thu |
| Column5 | Tram | Mã trạm |
| Column6 | (than đầu ra) | Chủng loại sau phối trộn |
| Column7 | (than đầu vào) | Chủng loại/nguồn than cấu thành |
| Column9-14 | L_100, Ak, Vk, Sk, Qk, L_NT | Khối lượng quy 100%, độ tro,
  độ ẩm/chất bốc, lưu huỳnh, nhiệt lượng, khối lượng nghiệm thu |
| Column18 | Cảng | "Cảng chính" → cờ CC |

Query `Bán` (trong QTTPT 2026.xlsx) gộp `Tồn TT + PA (2) + HHKK + HHB +
Tồn TN + XCN + NCN` rồi tính:
`L_B = L_TT + L_PA − L_HHB − L_KK − L_TTN + L_NCN − L_XCN`

**Đã xác nhận đầy đủ ý nghĩa từng số hạng (2026-07-08):**
- `L_TT` = Lượng tồn **tháng trước** (tồn **đầu** kỳ)
- `L_TTN` = Lượng tồn **tháng này** (tồn **cuối** kỳ)
- `L_PA` = phát sinh từ phương án phối trộn (Module 4)
- `L_HHB` = Hao hụt **bán** (KHÔNG phải "hao hụt bốc" — xem mục 6)
- `L_KK` = Hao hụt kiểm kê
- `L_NCN` / `L_XCN` = Nhập chuyển nguồn / Xuất chuyển nguồn

Với 2 số hạng đầu/cuối kỳ đã rõ, công thức là 1 **cân đối kho chuẩn**:
`Lượng bán = Tồn đầu + Nhập (PA + chuyển nguồn vào) − Xuất chuyển
nguồn ra − Hao hụt (bán + kiểm kê) − Tồn cuối` — tức suy ra từ đẳng
thức `Tồn cuối = Tồn đầu + Nhập − Xuất − Hao hụt`, hợp lý về mặt
nghiệp vụ, không còn là suy đoán rời rạc từng biến như trước.

## 5. Hàng nhập

- `HÀNG NHẬP\Hàng nhập 2026.xlsx` (sheet1, phẳng): mỗi dòng 1 lô hàng —
  `Trạm, Ngày hđ, Ngày GN, Chủng loại (x2), Tàu, Nguồn than, Lượng
  chưa QA, Lượng HĐ, KL TT, Lượng CN (chưa quy ẩm/đã quy ẩm/QA),
  % HAO HỤT, Đơn giá, Tiền than, CP Khác, Cước VC, BH`.
- File từng lô (vd. `SK02 BN 2638 PHOENIX 01.05.xlsx`) có 9 sheet:
  `BKHN` (Bảng sao kê hàng nhập/mua — nguồn, số hoá đơn, lượng theo
  HĐ/BBGN, đơn giá, tiền hàng, thuế, chi phí vận chuyển/kẹp
  chì/bảo hiểm), `PNK` (phiếu nhập kho), `BB KL` (biên bản khối
  lượng), `CA`, `NPHH`, `BBGĐ` (biên bản giám định), `BBGN`/`BBGN (2)`
  (biên bản giao nhận). Không có Power Query nào tự động gộp các file
  lô này vào `Hàng nhập 2026.xlsx`, nhưng **có 1 tool riêng ngoài
  Excel** làm việc này bán tự động — xem mục 5b.

### 5b. Tool gộp BKHN đang dùng — `bkhn_td_gui.py`

Vị trí: `C:\Users\ADMIN\OneDrive\Work\gopshetthuy\bkhn_td_gui.py` (app
PyQt6 độc lập, không thuộc repo này). Việc nó làm:
- Quét 1 thư mục (có thể đệ quy) chứa các file lô `.xlsx/.xls/.xlsm`,
  mỗi file 1 lô hàng (giống `SK02 BN 2638 PHOENIX 01.05.xlsx`).
- Với mỗi file: tự tìm sheet đích (ưu tiên tên chứa "01SST nhập kho",
  fallback "BKHN", fallback sheet đầu tiên không phải "foxz") rồi
  **định vị ô theo nội dung** (`find_cell_openpyxl` tìm chuỗi như "Số",
  "Mẫu:", "Tổng cộng", "Phí kẹp", "Ak:", "Vk:", "wtp:", "qk:", "sk:")
  chứ không dựa vào toạ độ cố định — cùng triết lý chống-vỡ-khi-đổi-
  layout mà `import_from_excel.py` của Module 1 đang dùng (tìm theo
  nội dung ô "Cộng"/"Số dư đầu kỳ").
- Có **2 nhánh layout** tuỳ file có ô "Phí kẹp" hay không (2 mẫu BKHN
  khác nhau đang tồn tại song song) — mỗi nhánh tính `hao_hut`/
  `hao_hutQA` khác công thức nhau:
  - Nhánh không có "Phí kẹp": `hao_hut = luong_CNchuaQA − luong_HD`,
    `hao_hutQA = luong_NK − luong_CNchuaQA`.
  - Nhánh có "Phí kẹp": `hao_hut = luong_NK − luong_HD`, còn
    **`hao_hutQA` bị để cứng = 0.0 — không tính** (lỗ hổng: nhánh
    layout này thiếu dữ liệu độ ẩm đầu vào để tính hao hụt quy ẩm).
  - **Đính chính (2026-07-08, đã chạy thử `parse_file()` thật trên
    `SK02 BN 2638 PHOENIX 01.05.xlsx`)**: ghi chú trước đó nói file
    này khớp nhánh "Phí kẹp" là **SAI** — nhầm chuỗi tìm kiếm "Phí
    kẹp" (`find_cell_openpyxl(ws, "D1:D50", "Phí kẹp")`) với nhãn cột
    "Kẹp chì (đồng)" thấy trong file, 2 chuỗi khác nhau nên không
    khớp. File này thực ra rơi vào **nhánh không có "Phí kẹp"**, tính
    ra `hao_hutQA` **thật** (không phải giá trị cứng 0.0) = 0.0 (đúng
    bằng 0 cho lô hàng cụ thể này, không phải placeholder). Đã chạy
    thử tiếp trên cả 97 file thật trong thư mục
    `HÀNG NHẬP\T5\HÀNG NHẬP T5.26` (dry-run) — **cả 97 file đọc được,
    không lỗi** — chưa xác định được có file nào trong bộ dữ liệu thật
    thực sự rơi vào nhánh "Phí kẹp" (hao_hutQA=0 giả) hay không, cần
    kiểm tra thêm khi có nhiều dữ liệu hơn (các trạm/tháng khác).
- Gộp tất cả file trong thư mục thành 1 bảng phẳng (`COLUMNS`: so_HD,
  ngay_HD, so_PNK, chung_loai, phuong_tien, luong_chuaQA, luong_HD,
  luong_CNchuaQA, luong_NK, hao_hut, hao_hutQA, tien_than, tong_CP,
  vc, bh, kc, vcbx, phicanthan, vun_gom, aK, vK, wtP, qK, sK) rồi xuất
  ra 1 file Excel — chính là
  `HÀNG NHẬP\T5\HÀNG NHẬP T5.26-KD THAN TÂN ĐỨC.xlsx`.

**Đã xác nhận đầy đủ (2026-07-08)** — thay cho khoảng trống nêu ban
đầu, xem qua trình bày lại chi tiết trong `CLAUDE.md` mục 5 "Module 3
(hàng nhập)":

- **"ĐN QÂ" (Quy ẩm đầu nguồn)** là **1 cột chèn TAY** vào file đầu ra
  của `bkhn_td_gui.py` (chèn giữa `luong_HD` và `luong_CNchuaQA`) —
  KHÔNG có trong `COLUMNS` gốc của tool, KHÔNG trích xuất được từ file
  BKHN thô. Là 1 **khối lượng (tấn)**, cùng đơn vị với `luong_HD`/
  `luong_NK` — **không phải phần trăm** như suy đoán ban đầu.
- **Công thức đã xác nhận** (kiểm chứng khớp đến từng đồng bằng 2 file
  thật độc lập cho cùng 1 lô hàng, so_HD=1007, trạm Tân Đức, tháng
  5/2026 — `HÀNG NHẬP T5.26-KD THAN TÂN ĐỨC.xlsx` và `Hàng nhập
  2026.xlsx` sheet T5):
  ```
  hao_hut    = luong_CNchuaQA − ĐN_QÂ
  hao_hutQA  = ĐN_QÂ − luong_HD
  ```
  Công thức `hao_hut = luong_CNchuaQA − luong_HD` trong `bkhn_td_gui.py`
  (nhánh không "Phí kẹp") chỉ là giá trị **tạm thời** trước khi điền
  ĐN QÂ, không phải giá trị dùng để đối chiếu kế toán.
- **Không phải than nào cũng cần ĐN QÂ** — chỉ **than nhập khẩu** mới
  cần quy ẩm; than nội địa (các loại Cám) và **phiếu điều chỉnh giá**
  vốn dĩ **không cần điền** cột này, đây là thiết kế đúng của dữ liệu
  nguồn, không phải thiếu sót cần người dùng bổ sung — quan trọng khi
  thiết kế gate nhập liệu (không được coi "thiếu ĐN QÂ" luôn luôn =
  "cần chặn lại chờ nhập tay").
  **Đính chính (2026-07-10, kiểm chứng bằng 3 file BKHN thật + file
  gộp `Hàng nhập 2026.xlsx`)**: phát biểu "than nội địa không có cột
  này" ở trên **không chính xác** — mẫu BKHN (`SK01 HP 5902...xlsx`,
  than trong nước "Cám 5b.1") **vẫn có đủ khối cột** `Khối lượng thanh
  toán đầu nguồn / KL nhập kho quy ẩm tiêu chuẩn / KL hao hụt nhập kho
  / Hao hụt quy ẩm / Lượng thực nhập quy ẩm 8,5` (U31:Y31) — **cùng 1
  mẫu form** với file nhập khẩu (`SK02 BN 2638 PHOENIX...xlsx`). Khác
  biệt thật: cột "Hao hụt quy ẩm" **để trống** ở dòng than nội địa
  (X34 trong SK01), có giá trị thật ở dòng than nhập khẩu (X39=73.59
  trong SK02). Rà toàn bộ 18 dòng thật trong `HÀNG NHẬP T5.26-KD THAN
  TÂN ĐỨC.xlsx`: mọi dòng "Than cám..." (nội địa) để trống cột "ĐN
  QÂ", mọi dòng "Than nhiệt xuất xứ..." (nhập khẩu) đều được điền tay
  — quy tắc nghiệp vụ "chỉ nhập khẩu mới cần ĐN QÂ" **vẫn đúng trong
  thực tế vận hành**, chỉ sai ở chỗ nói mẫu form "không có cột" (mẫu
  có sẵn cột cho cả 2 loại, chỉ khác ở việc điền hay không điền).
- **Phát hiện mới (2026-07-10) — lý do THẬT SỰ vì sao ĐN QÂ phải nhập
  tay**: đọc trực tiếp mã nguồn `bkhn_td_gui.py` (người dùng cung cấp)
  và chạy thử `parse_file()` trên cả 2 file BKHN thật, phát hiện logic
  tự tính `hao_hutQA` của tool **không đáng tin** ở cả 2 nhánh:
  - Nhánh có nhãn "Phí kẹp" ở cột D (khớp SK01, than nội địa — trước
    đây `TASK.md`/`md-01` ghi "chưa xác định được file nào rơi vào
    nhánh này", nay đã có ví dụ thật): `hao_hutQA` bị **hard-code =
    0.0**, không tính.
  - Nhánh không có "Phí kẹp" (khớp SK02, than nhập khẩu): công thức
    `hao_hutQA = luong_NK − luong_CNchuaQA` cho ra **0.0** vì 2 biến
    này vô tình cùng trỏ tới 1 ô Excel (cột G, giá trị 1949.14 lặp lại
    ở nhiều dòng chi phí trong bảng BKHN) — không phải 0 thật.
  Tức **cả 2 nhánh của tool đều luôn cho `hao_hutQA=0.0`** dù lý do
  khác nhau — đây là lý do cụ thể (không phải chỉ "thiếu cột") khiến
  con người phải tự đọc số liệu quy ẩm thật (nằm sẵn ở khối cột U-Y
  của chính sheet BKHN, vd X39=73.59 ở SK02) rồi gõ tay ĐN QÂ đúng.
  Phần tính phụ phí (tiền than/VC/KC/BH/VCBX/cân than/vun gom) của
  tool đã kiểm chứng khớp tuyệt đối 100% với dòng "Tổng cộng" ở cả 2
  file — không có vấn đề, chỉ riêng phần lượng/quy ẩm là không đáng
  tin cậy khi tự động.
- Nguồn dữ liệu **tự động** cho "ĐN QÂ" (không phải công thức dùng nó)
  **vẫn chưa xác định** — người dùng vẫn điền tay, xác nhận lại đúng
  vậy 2026-07-10.

Ở thư mục `gopshetthuy` còn có các notebook biến thể theo trạm khác:
`BKHN-TĐ.ipynb`, `BKHN-TĐ2.ipynb`, `BKHN-VC.ipynb`, `BKHN-VC2.ipynb`
(và 1 bản `copy`) — tức **mỗi trạm có 1 layout BKHN hơi khác nhau**,
`bkhn_td_gui.py` mới chỉ đóng gói logic của trạm Tân Đức (TĐ) thành
GUI dùng lại được; các trạm khác vẫn ở dạng notebook chạy tay — **vẫn
cần hỏi người dùng** có nên tổng quát hoá cho mọi trạm hay không.

### 5c. "Hàng nhập 2026.xlsx" — cấu trúc thật (đính chính khảo sát ban đầu)

Khảo sát ban đầu ở mục 5 (dòng header ở dòng 1, sheet "Sheet1" phẳng)
là **SAI** — có thể do khảo sát nhầm phiên bản/1 phần khác của file.
Cấu trúc thật (khảo sát lại 2026-07-08 trên bản sao trực tiếp từ file
đang dùng):

- **Nhiều sheet theo tháng**, đặt tên `T1`..`T12` (cùng quy ước với
  `Sổ theo dõi PA trạm`), **cộng thêm biến thể `<tên sheet> (DD)`**
  (vd `T5 (DD)`) = **các lô hàng đang đi đường, chưa về kho** tại thời
  điểm chốt (xác nhận từ người dùng) — KHÔNG được coi là hàng đã nhập
  kho, không import các sheet này vào `hang_nhap`.
- **Header nằm ở DÒNG 3**, không phải dòng 1 (dòng 1-2 là dòng tổng
  hợp/tiêu đề riêng — dòng 1 thậm chí cũng có 1 ô ghi "Trạm" dễ gây
  nhầm khi dò theo nội dung, cần khớp thêm cột "Số HĐ" mới chắc chắn
  đúng dòng).
- **Cột từ F trở đi** của file này **giống 1:1 (chỉ lệch offset 5
  cột)** với cột A trở đi của file đầu ra `bkhn_td_gui.py` (vd
  `...-KD THAN TÂN ĐỨC.xlsx`) — xác nhận từ người dùng. Tức file này
  là nơi **gộp dữ liệu từ nhiều trạm** (mỗi trạm dán dữ liệu luồng-1
  của mình vào), thêm 4 cột alias đầu (`Biểu 8`, `Biểu 7`, `Kho`,
  `NXT`) suy ra qua ngân hàng tên than.
- Cột `HH`/`HHQA` trong file này **đã được tính sẵn** theo đúng công
  thức đã xác nhận ở mục 5b — không cần tính lại khi import.
- **Không phải dòng nào cũng có "Lượng đầu nguồn QA"** (kiểm tra thật:
  chỉ 83/191 dòng trong sheet T5 có giá trị) — nhưng đây **không phải
  thiếu sót**, mà đúng vì không phải than nào cũng cần quy ẩm (xem
  mục 5b). Do đó **luồng 2 vẫn ghi thẳng vào CSDL chính thức, không
  qua bước nháp** — khác hẳn với ban đầu tưởng là "cần gate giống
  luồng 1", xem `CLAUDE.md` mục 5 "Module 3".
- **Đính chính thêm (2026-07-08): header có 8 cột NỮA sau "KC"** mà
  khảo sát ở mục 5c ban đầu (viết `import_hang_nhap_luong2.py`) đã bỏ
  sót — `VCBX | Cân than | Vun gon | AK | V | W | Q | S`. Đã sửa
  `ANH_XA_COT` để đọc đủ (model đã có sẵn field `vcbx`/`phicanthan`/
  `vun_gom`/`ak`/`vk`/`wtp`/`qk`/`sk` từ trước, chỉ chưa được điền).
- **Header đầy đủ đã kiểm chứng bằng file thật (2026-07-10)**, đúng
  33 cột dòng 3 của sheet `T1`: `Trạm | Biểu 8 | Biểu 7 | Kho | NXT |
  Số HĐ | Ngày | Số PNK | CL | pt | Lg chưa QA | Lượng HĐ | Lượng đầu
  nguồn QA | Lượng CN chưa QA | Lượng NK | HH | HHQA | Tiền than | T
  CP | VC | BH | KC | VCBX | Cân than | Vun gon | AK | V | W | Q | S |
  (cột trống) | TD | TD/PT`.
- **Cơ chế VLOOKUP Biểu 8/Biểu 7/TD/TD-PT từ cột `NXT` qua sheet `Tên
  cám` — đã xác nhận bằng số thật (2026-07-10)**, đúng như người dùng
  mô tả: cột `NXT` là khoá tra cứu vào cột `Than tại NXT` của sheet
  `Tên cám`; `Biểu 8`/`Biểu 7` lấy thẳng từ 2 cột cùng tên; `TD` lấy
  từ cột `TD` (giá trị chuỗi `'TD'` hoặc rỗng, không phải boolean);
  `TD/PT` lấy từ cột `Tên TD` khi có `TD`, ngược lại mặc định hiển thị
  lại giá trị `Biểu 7`. Ví dụ đối chiếu đúng: dòng `NXT="Cám 4a.1"` →
  `Tên cám` hàng tương ứng cho `Biểu 8=' - Cám 4a.1'`, khớp tuyệt đối
  với dữ liệu trong `T1`; dòng `NXT="Cám 4b.1 BT (tự doanh)"` → `Tên
  cám` có `TD='TD'`, khớp đúng cột `TD`/`TD-PT` trong `T1`.
- **Sheet `T<n> (DD)` — đã kiểm chứng cấu trúc thật (2026-07-10)**:
  không hiếm như ghi chú cũ ("hiếm khi cần nhập") — riêng `T1 (DD)` đã
  có **23 dòng dữ liệu thật** trong 1 tháng. Header khác `T<n>` chính:
  **không có cột "Lượng đầu nguồn QA"** (hợp lý — hàng đi đường chưa
  nhập kho nên chưa có số liệu quy ẩm cuối cùng).
- File thật còn có **~20 sheet ẩn khác chưa từng ghi trong tài liệu**:
  `LastM`, `LastDD`, `Sheet4`, `LastT`, `CBC`, `Done`, `Sheet6`, `ĐG VC
  mua`, `TH thang`, `TD`, `TD (2)`, `CB`, `CB (2)`, `TH`, `CL nhập`,
  `Nhap1`, `T1  ` (có khoảng trắng cuối tên, khác `T1`), `2`, `3`,
  `Sheet1`, `,,,`, `Sheet3` — có vẻ là bảng trung gian/pivot/nháp
  Power Query cũ. **CHƯA XÁC NHẬN** vai trò, không ảnh hưởng luồng 2
  chính (`T1`..`T12` + `T<n> (DD)` + `Tên cám`).

### 5d. Đối chiếu "Sổ chi tiết vật tư" (Module 1) ↔ "Hàng nhập" (Module 3) — xác nhận cách tính phụ phí Nhập

Người dùng chỉ ra ví dụ cụ thể để đối chiếu: kho **Tân Đức**, tháng 3,
lô **"Than Anthracite Lào - Lô hàng 06/T03/2026 (Tàu GOLDEN STAR)"**,
số HĐ **680**. So sánh sheet "GOLDEN STAR" trong `NXT Tân Đức 3.xlsx`
(Module 1) với dòng số HĐ=680 trong sheet `T3` của `Hàng nhập
2026.xlsx` (Module 3) — **khớp tuyệt đối từng đồng**:

| | Sổ chi tiết vật tư (dòng, cột "Đơn giá") | Hàng nhập (cột) | Giá trị |
|---|---|---|---|
| Giá than | dòng chính, cùng dòng Lượng nhập=1.321,94 | `tien_than` | 3.170.394.291 |
| Bảo hiểm | dòng sau, nhãn "BH" | `bh` | 1.424.849 |
| Kiểm/cân | dòng sau, nhãn "KC" | `kc` | 329.077 |
| Vận chuyển + bốc xếp | dòng sau (không nhãn rõ, giữa "PT: HP 4852" và "BH") | `vcbx` | 6.213.118 |
| Cân than | dòng sau, nhãn "Cân than" | `phicanthan` | 1.321.940 |
| Cồn đống | dòng sau, nhãn "Cốn đống" (lỗi chính tả trong Excel gốc) | `vun_gom` | 1.784.610 |

**Kết luận rút ra được (thay thế hoàn toàn giả định cũ trong
`import_from_excel.py::MA_PHU_PHI_MAC_DINH`)**:

1. **1 giao dịch Nhập trong Sổ chi tiết vật tư trải trên NHIỀU dòng
   liên tiếp** (không phải 1 dòng như code hiện giả định) — dòng đầu
   có Ngày/Chứng từ/Diễn giải/Lượng/Đơn giá than; các dòng sau chỉ có
   cột "Đơn giá" (chứa SỐ hoặc TEXT là nhãn phí) + "Số tiền" tương
   ứng, "TK đối ứng" giữ NGUYÊN mã đối tác (vd `331`) xuyên suốt cả
   khối — **KHÔNG đổi thành "BH"/"KC" như code cũ giả định**. Rà toàn
   bộ `NXT/Tháng *.2026/*.xlsx`: mọi trường hợp "TK đối ứng" literal
   = "BH"/"KC" đều có Lượng/Số tiền = 0 (dòng mẫu/rỗng) — nhãn phí thật
   sự có số tiền luôn nằm ở cột Đơn giá như trên.
2. **Không cần đoán "gắn vào giao dịch Nhập gần nhất cùng ngày"** —
   số liệu phụ phí ĐÃ CÓ SẴN, đúng theo từng lô, trong bảng `hang_nhap`
   (Module 3, luồng 2). Thiết kế đúng: khi Module 1 đọc 1 khối Nhập
   trong Sổ chi tiết vật tư, đối chiếu/join với `hang_nhap` theo
   (trạm + số HĐ) hoặc (trạm + phương tiện — text "PT: HP 4852" khớp
   `hang_nhap.phuong_tien`) thay vì tự suy luận lại từ các dòng rời
   rạc. Việc code lại `parse_sheet()` theo hướng này **chưa làm** —
   xem `TASK.md` Phase 0.4.

### 5e. "Phiếu điều chỉnh" — đính chính (2026-07-10, sai so với ghi chú cũ)

Ghi chú cũ (`CLAUDE.md` mục 5, `md-01` mục 5) từng khẳng định: *"phiếu
điều chỉnh giá (chỉ chỉnh tiền, không liên quan lượng) vốn dĩ không có
cột [ĐN QÂ]"*. Kiểm chứng bằng file thật `SK19 ĐC tăng lượng SIRIUS
7.5.xlsx` (người dùng cung cấp) cho thấy **phát biểu này không đúng
cho mọi trường hợp**:

- Ô diễn giải (D8) của file ghi rõ: *"Điều chỉnh TĂNG KHỐI LƯỢNG,
  thành tiền và tiền thuế theo hóa đơn số 1072..."* — tên file cũng
  ghi rõ "ĐC tăng lượng". File có 3 dòng con theo phương tiện (`BN
  2509`/`BN 2595`/`BN 2633`), tổng lượng thật **147,5 tấn** (không
  phải 0).
- Đối chiếu với `Hàng nhập 2026.xlsx` (bản gộp): dòng `so_HD=1072`
  trong đó có **toàn bộ cột lượng = 0**, chỉ có `tien_than=459.201.130`
  (khớp đúng tổng tiền của SK19) — 2 trong 3 phương tiện của SK19
  (`BN 2595`, `BN 2633`) trùng đúng phương tiện của 2 dòng nhập đã có
  sẵn trước đó trong cùng file (HĐ 970, HĐ 1006, cùng tàu STAR
  SIRIUS) — xác nhận đây là **điều chỉnh tăng thêm lượng cho các lô đã
  ghi nhận trước đó**, không phải 1 lô nhập độc lập.
- **Đã xác nhận với người dùng đây là giới hạn có chủ đích, không phải
  lỗi**: quy trình Excel hiện tại chỉ cần tổng tiền/tổng lượng của cả
  phiếu điều chỉnh để đưa vào sổ, không cần tách theo từng lô con —
  tool `bkhn_td_gui.py` phản ánh đúng nhu cầu đó.
- **Ý nghĩa cho CSDL mới — CHƯA CHỐT, cần quyết định khi làm Module
  3**: giữ nguyên hành vi cũ (1 giao dịch điều chỉnh ghi tổng tiền,
  lượng=0, không gắn xuống lô gốc) hay tách chi tiết theo từng lô con
  để cộng đúng lượng vào đúng lô gốc (chính xác hơn cho tồn kho/giá
  vốn theo lô, nhưng cần nhập tay chi tiết hơn mức hiện tại). Không tự
  chọn phương án — để người dùng quyết định.
- Phát biểu đúng lại: **"phiếu điều chỉnh" là 1 NHÓM nhiều loại khác
  nhau** (chỉnh giá thuần tuý, chỉnh cả lượng...), phải phân loại theo
  nội dung diễn giải thực tế, không giả định mặc định là chỉ chỉnh
  tiền.

## 6. Ghi chú tên các đối tượng nghiệp vụ

**Đã xác nhận với người dùng (2026-07-08)** — thay cho các suy đoán
trước đó:
- `KVCP` = **Kho vận Cẩm Phả** (KHÔNG phải "khu vực cảng" như suy đoán
  ban đầu).
- `HHB` = **Hao hụt bán** (KHÔNG phải "Hao hụt bốc" như suy đoán).
- `HHKK` = **Hao hụt kiểm kê** (suy đoán ban đầu đúng).
- `XCN` = **Xuất chuyển nguồn** (KHÔNG phải "Xuất chuyển nội" như suy
  đoán).
- `NCN` = **Nhập chuyển nguồn** (KHÔNG phải "Nhập chuyển nội" như suy
  đoán).
- `QTTPT` = **Quyết toán than pha trộn** (KHÔNG phải "Quyết toán tổn
  phí" như dùng nhầm trước đó — đã sửa lại tên Module 7 ở mọi nơi
  trong `CLAUDE.md`/`TASK.md`).

- `THP` = **Than Hải Phòng** — tên công ty sở tại (đơn vị cấp dưới/chi
  nhánh vận hành thực tế của "Công ty CP Kinh doanh than Miền Bắc -
  Vinacomin" tại khu vực Hải Phòng), **xác nhận 2026-07-08** (KHÔNG
  phải "Trạm Hải Phòng" như suy đoán ban đầu). Xác nhận thêm bằng dòng
  tiêu đề thật trong cả 2 file BM7/BM8 dưới đây: `"CÔNG TY KD THAN HẢI
  PHÒNG"` / `"Công ty kinh doanh than Hải Phòng"`.
**Lưu ý quan trọng (xác nhận 2026-07-08): cả 3 file BM7/BM8/BM PT-TD
dưới đây đều là file "-print" — tức bản IN RA/XUẤT RA cuối cùng, KHÔNG
phải nguồn dữ liệu để đọc vào hệ thống.** Vai trò của chúng trong kiến
trúc là **layout đích** mà Module 9 phải tái tạo khi xuất báo cáo,
không phải input cho bất kỳ module import nào.

- `BM7` = **Biểu 07-TMB**, đích thật (**xác nhận 2026-07-08**):
  `C:\Users\ADMIN\OneDrive\8. Thủy\KHO NĂM 2026\Quyết toán\Bao cáo NXT
  Biểu 07-TMB-print.xlsx`. Tên đầy đủ trên biểu: **"BÁO CÁO CHI TIẾT
  NHẬP XUẤT TỒN KHO"** — NXT **theo danh mục/chủng loại than** (nhóm
  theo khoảng độ tro Ak, toàn công ty, KHÔNG tách theo trạm). Sheet:
  `LK` (luỹ kế cả năm) + `T0`..`T4`... (từng tháng, `T0` = tháng 12
  năm trước dùng làm tồn đầu năm) + `Query1`. Cấu trúc cột rất chi
  tiết — 4 khối lớn mỗi sheet tháng:
  - **Tồn đầu kỳ**: Tổng cộng / Trong kho / Đi đường / Gửi bán.
  - **Nhập trong kỳ**: Mua KVCP, Mua kho vận Đá Bạc, Mua khác trong
    TKV, Tổng nhập mua Vinacomin, Mua đơn vị khác, Mua nội bộ Miền
    Bắc, Hao hụt khâu nhập hàng, Nhập chênh lệch do quy ẩm, Nhập nội
    bộ đơn vị, Nhập chế biến, Nhập pha trộn, Nhập thừa kiểm kê, Nhập
    khác, Nhập chuyển đổi, Tổng nhập trong kỳ.
  - **Xuất trong kỳ**: Xuất bán nội bộ TKV, Xuất bán tự doanh, Tổng
    xuất bán, Xuất bán nội bộ Miền Bắc, Xuất nội bộ đơn vị, Xuất chế
    biến, Xuất pha trộn, Xuất thiếu kiểm kê, Xuất hao hụt bán, Xuất
    chuyển đổi, Xuất khác, Tổng xuất.
  - **Tồn cuối kỳ**: Tổng cộng tồn, Tồn trong kho, Tồn đi đường, Tồn
    gửi bán.
  Mỗi cột con có `Lượng` + `Tiền` (nhiều cột còn có thêm `Chi phí nhập
  kho`) — đây chính là layout đích cho Module 9.
- `BM8` = **Biểu 08-TMB**, đích thật (**xác nhận 2026-07-08**):
  `C:\Users\ADMIN\OneDrive\8. Thủy\KHO NĂM 2026\Quyết toán\Biểu 08
  TMB-print.xlsx`. Tên đầy đủ: **"BÁO CÁO NHẬP XUẤT TỒN KHO - CHI TIẾT
  CÁC TRẠM, CỬA HÀNG"** — khác BM7 ở chỗ tách **theo từng trạm/cửa
  hàng** (BM7 là NXT toàn công ty theo chủng loại, BM8 là NXT chi
  tiết theo trạm). Sheet: `LK`, `T0`..`T4`..., `GOP` (gộp). Cột đầu kỳ
  tương tự BM7 (Tổng cộng/Trong kho/Đi đường/Gửi bán) rồi các nguồn
  nhập: Nhập mua, Nhập nội bộ MB, Nhập chế biến, Nhập pha trộn, Nhập
  nội bộ công ty, Nhập lại hàng ĐĐ...
- `BM PT/TD` (nhắc trong `CLAUDE.md`) = 2 biểu **theo mẫu Tập đoàn**
  (không phải "-TMB" như BM7/8) — đích thật (**xác nhận 2026-07-08**):
  `C:\Users\ADMIN\OneDrive\8. Thủy\KHO NĂM 2026\THỐNG KÊ\Báo cáo NXT
  TD-CB (tháng)-print.xlsx`. Tiêu đề trên biểu: **"BÁO CÁO CHỦNG LOẠI
  THAN, SẢN PHẨM NGOÀI TIÊU CHUẨN THAN, TIÊU THỤ, TỒN KHO"**, do
  "TẬP ĐOÀN CÔNG NGHIỆP THAN-KHOÁNG SẢN VIỆT NAM / CÔNG TY CỔ PHẦN
  XUẤT NHẬP KHẨU THAN - VINACOMIN" quy định mẫu. `TD` = **Tự doanh**,
  `PT` = **Pha trộn** — 2 luồng kinh doanh tách riêng, mỗi luồng có
  sheet riêng theo kỳ (`TD0`/`PT0`, `TD1`/`PT1`...) cùng layout: Số
  TT, Tên sản phẩm, Mã sản phẩm, ĐVT, Than tồn đầu năm báo cáo (Tổng
  số + breakdown), Than nhập trong kỳ (Than sạch SX từ than nguyên
  khai/BTP/đất đá lẫn than, Mua trong TKV, Mua đơn vị khác, Nhập nội
  bộ TMB, Nhập sau tuyển NC, Nhập sau pha trộn...). Có thêm sheet tổng
  hợp `Biểu NXT (điện)`, `Biểu NXT (tự doanh)`, `Biểu NXT (tổng)`,
  `PT_G`/`TD_G` (gộp), `NXT-TD`/`NXT-PT`.

**Đã xác nhận thêm với người dùng (2026-07-10)** — 3 điểm còn treo từ
`QTTPT_2026.m`/`THP_KVCP_2026.m` (xem mục 8-9 và `CLAUDE.md` mục 6):

- **Sheet `CN`** (nguồn `L_XCN`/`L_NCN` theo lô, dùng trong
  `QTTPT_2026.m`) **chính là bảng GỘP (union) của `X_CN` và `N_CN`** —
  2 tập dòng dữ liệu Xuất chuyển nguồn/Nhập chuyển nguồn được lưu
  chung 1 sheet, không phải "2 cách đọc khác nhau của cùng 1 dòng" như
  suy đoán ban đầu ở mục 8/`CLAUDE.md`.
- **Điều kiện `STTPA<0`** trong query `Bán` của `THP_KVCP_2026.m`
  **lọc ra các cám thành phẩm đã pha trộn từ tồn năm trước** — những
  dòng không có 1 phương án (PA) thật trong năm hiện tại để đánh số
  `STTPA` dương (qua `Index` query), nên được gán 1 giá trị âm làm cờ
  đánh dấu "hàng tồn năm trước". Giải thích được vì sao công thức nhân
  `L_TTT` (tồn đầu kỳ) chứ không phải `L_B` (lượng bán) — với nhóm này
  "tồn đầu kỳ" mới là số lượng còn ý nghĩa để tính bình quân gia quyền
  chất lượng.
- **`Bieu35a10`/`Bieu45a14`** (named range trong `THP_KVCP_2026.m`) là
  **các biểu báo cáo riêng theo TỪNG CÁM THÀNH PHẨM** (Biểu 35 dành
  cho sản phẩm "5a.10", Biểu 45 dành cho "5a.14") — không phải mã
  trạm/khu vực như suy đoán ban đầu. Hậu tố `ĐHP`/`ĐTB`/`ĐVA` (và
  `ĐHD` ở "Cám 6b.1 ĐHD") là phần TÊN BIẾN THỂ sản phẩm, **dùng để
  biết bán cho đâu** — phân biệt cùng 1 chủng loại than (cùng khoảng
  Ak) theo **đích bán/kênh bán khác nhau**, không phải biến thể chất
  lượng hay kho vật lý khác nhau. Cơ chế **chuyển nguồn (XCN/NCN) phục
  vụ trực tiếp việc phân loại theo đích bán này** — khi 1 lô cần
  chuyển từ nguồn/trạm này sang phục vụ đích bán khác thì ghi nhận qua
  XCN/NCN. Ý nghĩa chữ viết tắt cụ thể (`ĐHP`/`ĐTB`/`ĐVA`/`ĐHD` là
  viết tắt của đích bán/khách hàng nào) **vẫn CHƯA XÁC NHẬN**, nhưng
  không ảnh hưởng thiết kế `san_pham` (chỉ cần lưu đúng chuỗi tên).

## 7. File Power Query M gốc đã trích xuất

Lưu tại `md/power_query/`:

- `Cac_bieu_2026-M.m` — từ `Quyết toán\Các biểu 2026-M.xlsx`
- `QTTPT_2026.m` — từ `QTTPT 2026\QTTPT 2026.xlsx`
- `THP_KVCP_2026.m` — từ `QTTPT 2026\KVCP\THP.Biểu mẫu Quyết toán KVCP 2026.xlsx`
- `So_theo_doi_PA_tram_2026.m` — từ `Sổ theo dõi PA trạm 2026.xlsx`
- `Tinh_ton_2.m` — từ `QTTPT 2026\Tính tồn 2.xlsx` (xem mục 8)

(File `Cân bằng chất.xlsx` không có Power Query M — dữ liệu ở đó chủ
yếu là công thức Excel tính tay, không phải Get&Transform. Đây VẪN là
file **chính thức** — xem mục 2 bảng sheet, kết quả phục vụ trực tiếp
sheet `DCCL` trong `THP.Biểu mẫu Quyết toán KVCP 2026.xlsx`.)

## 8. `Tính tồn 2.xlsx` — bộ tính phân bổ Tồn/HHB/HHKK theo lô

File này (`QTTPT 2026\Tính tồn 2.xlsx`, không nằm trong 4 file quyết
toán được liệt kê ban đầu, nhưng được `QTTPT 2026.xlsx` dùng làm đầu
vào cho các sheet `Tồn`/`HHB`/`HHKK`) làm 1 việc khác hẳn các query đã
mô tả ở mục 4-5: **phân bổ (allocation)**, không phải tổng hợp
(aggregation) đơn thuần.

Bối cảnh: kiểm kê/hao hụt được xác định **ở mức sản phẩm đầu ra**
(1 trạm, 1 chủng loại than, 1 tháng — vd "CC / 5a.10 ĐTB / tháng 5":
tổng tồn X tấn, tổng hao hụt bán Y tấn...), nhưng hạch toán giá vốn
và chất lượng cần biết **từng lô than cấu thành** (mỗi dòng PA gắn 1
"Data.Column7" = 1 lô/nguồn than cụ thể với Ak/Vk/Sk/Qk riêng, vì
cùng sản phẩm đầu ra "5a.10 ĐTB" có thể được phối trộn từ nhiều lô
than nhập khác nhau ở các thời điểm khác nhau). Bài toán: chia X tấn
tồn / Y tấn hao hụt đó **xuống các dòng lô (phương án) cấu thành**.

**Quy tắc phân bổ đã được xác nhận (2026-07-08):**
- **Tồn**: phân bổ vào các **phương án (PA) gần nhất** (tính đến thời
  điểm chốt) — tức lô nhập/phối trộn gần đây nhất được ưu tiên coi là
  còn tồn (kiểu LIFO theo phương án, không phải theo lô nhập vật lý).
- **HHKK** (hao hụt kiểm kê): phân bổ vào các PA **gần nhất so với
  ngày kiểm kê** — không phải gần nhất tính đến hiện tại, mà gần nhất
  so với đúng ngày thực hiện kiểm kê kho.
- **HHB** (hao hụt bán — xem mục 6, KHÔNG phải "hao hụt bốc"): phân bổ
  vào các PA **gần nhất trong số còn lại**, sau khi đã trừ đi phần đã
  gán cho Tồn và HHKK — duyệt gần nhất rồi lùi dần về trước
  (nearest-first, đi lùi theo thời gian) cho tới khi hết Y tấn cần
  phân bổ.

Tức thứ tự ưu tiên xử lý khi phân bổ 1 sản phẩm/tháng: **Tồn trước →
HHKK kế tiếp (neo theo ngày kiểm kê) → HHB phân vào phần PA còn lại,
duyệt từ gần nhất lùi về trước**. Điều này khớp với việc sheet
`Append1`/`LK` có cột luỹ kế giảm dần `L_B` theo từng SPT (waterfall
trừ dần theo thứ tự PA, không phải chia đều tỷ lệ).

Đẳng thức cân đối dùng xuyên suốt các sheet `Append1`, `Append2`,
`Check`, `C2`:

```
L_B = L_TT + L_NT − L_T − L_HH − L_KK − L_XCN + L_NCN
```

(`L_TT`=tồn đầu, `L_NT`=nghiệm thu/nhập, `L_T`=tồn cuối, `L_HH`=hao
hụt bốc, `L_KK`=hao hụt kiểm kê, `L_XCN`/`L_NCN`=xuất/nhập chuyển nội
bộ, `L_B`=lượng bán — cùng công thức đã thấy ở query `Bán` trong
`QTTPT_2026.m`, nhưng ở đây tính **theo từng dòng lô** rồi mới gộp
lên, chứ không tính thẳng ở mức tổng).

Các sheet trong file: `PA`/`PA2` (đầu vào — danh sách lô theo SPT),
`Tồn`/`HHB`/`HHKK`/`XCN` (kết quả phân bổ theo lô, đúng layout để dán
ngược vào các sheet cùng tên trong `QTTPT 2026.xlsx`), `Append1`/
`Append2`/`LK` (bảng trung gian tính luỹ kế/phân bổ tuần tự),
`Check`/`CheckKQ`/`Result`/`Result (KK)` (đối chiếu tổng phân bổ ra có
khớp tổng đầu vào theo (Tháng, Trạm, Sản phẩm) không — có 2 dòng đầu
mỗi sheet Result ghi rõ "Tháng X / Loại HHB (hoặc KK)" → xác nhận file
này **chạy thủ công lại mỗi tháng, chọn tham số Tháng + Loại (HHB hay
KK)**, không tự động hoá theo tháng.

**Đính chính (2026-07-10, kiểm chứng bằng file thật do người dùng
cung cấp)**: câu trên xếp `LK` chung nhóm "bảng trung gian" với
`Append1`/`Append2` — **SAI**. Theo xác nhận của người dùng và đối
chiếu số liệu thật: **`LK` là sheet ĐẦU VÀO** (Tháng, Trạm, Cám thành
phẩm, Tồn, HHKK, HHB nhập tay theo kết quả kiểm kê thực tế) — khớp
đúng vai trò bảng `KetQuaKiemKe` đã thiết kế ở Module 6, không phải
bảng trung gian. `Append1`/`Append2` mới là trung gian luỹ kế thật.
`Result` là **đầu ra** (kết quả phân bổ xuống từng dòng PA thành
phần, layout `SPT, N_HD, N_PT, N_NT, Tram, Data.Column6 (than ra),
Data.Column7 (than vào), L_100, Ak, Vk, Sk, Qk, Luong (lượng phân bổ),
STTPA, Cảng, Tháng`, kèm 2 dòng header riêng ghi rõ `Tháng=X` /
`Loại=HHB` (hoặc KK) đang chạy). `CheckKQ` đối chiếu tổng đầu vào
(cột C, từ `LK`) với tổng phân bổ ra (cột D, SUM theo `Result`) —
**đã thấy cả 2 trường hợp thật**: khớp tuyệt đối (`CC/5a.10 ĐHP`:
9=9, chênh lệch=0) và **không khớp/thiếu dữ liệu PA để giải thích
hết** (`VC/5a.14 ĐTB`: chỉ có tổng phân bổ ra, không có tổng đầu vào
để so — cột chênh lệch bỏ trống) — xác nhận cơ chế cảnh báo
`ton_chua_phan_bo`/`canh_bao` đã thiết kế ở Module 6 đang mô phỏng
đúng 1 tình huống có thật, không phải giả định lý thuyết.

Xác nhận thêm bằng số thật: 1 `STTPA` (1 phương án) có thể có **nhiều
dòng thành phần đầu vào khác nhau** trong `Result` (vd STTPA=312, ra
"5a.10 ĐHP", có 4 dòng `Data.Column7` khác nhau: Cám 5a.1/Cám
5a.3/than Mozambique/Cám 6a.1, mỗi dòng 1 lượng phân bổ riêng) — khớp
đúng mô hình `phuong_an` hiện tại (1 dòng = 1 cặp than ra + 1 than
vào, nhiều dòng cùng SPT khi phối trộn nhiều nguồn).

**Quy tắc làm tròn khi phân bổ — mới xác nhận (2026-07-10), CHƯA từng
ghi trong tài liệu cũ** (không có trong Power Query M vì đây là công
thức Excel tính tay ở `Append1`, không phải Get&Transform): sau khi
`Append1` tính lượng phân bổ thô cho từng dòng PA (theo thứ tự waterfall
đã mô tả ở trên) và làm tròn 2 chữ số mỗi dòng, tổng các dòng đã làm
tròn có thể lệch khỏi tổng thực tế 1 khoản nhỏ (bội số của 0,01) do
làm tròn cộng dồn. Cách xử lý: với mỗi dòng, tính
`delta = giá_trị_đã_làm_tròn − giá_trị_gốc`, xếp hạng (rank) các dòng
theo `delta`; nếu tổng làm tròn **thiếu** so với tổng thực → cộng
0,01 lần lượt theo rank **xuôi**; nếu **thừa** → trừ 0,01 lần lượt
theo rank **ngược**, cho tới khi tổng làm tròn khớp tổng thực. Đây là
1 biến thể của "phương pháp số dư lớn nhất" (largest remainder
method) quen thuộc trong bài toán phân bổ có làm tròn. **Đã xác nhận
ở mức nguyên tắc**, chi tiết cài đặt (chiều rank khi 2 dòng bằng
nhau, áp dụng cho cả 3 loại Tồn/HHKK/HHB hay chỉ áp dụng cho loại
đang tính) để dành khi bắt đầu code Module 6.

Ngoài các sheet đã liệt kê, file thật còn có thêm `PAKK`, `PL`,
`Sheet1` (ẩn) — **CHƯA XÁC NHẬN** vai trò cụ thể.

→ **Ý nghĩa cho thiết kế CSDL**: đây là lý do cụ thể để **không** áp
dụng tuyệt đối nguyên tắc "không lưu cứng số liệu suy ra được" — xem
nguyên tắc #2 đã sửa lại trong `CLAUDE.md` mục 2. Bảng phân bổ theo lô
này nên là 1 bảng snapshot lưu theo kỳ, có cờ đã chốt, không phải view
tính động.

## 9. `Cân bằng chất.xlsx` — khảo sát chi tiết (2026-07-10, file thật)

File này (đã xác nhận trước đó là bản **chính thức**, phục vụ trực
tiếp sheet `DCCL` — xem mục 6) không có Power Query M (công thức Excel
thuần). Đã khảo sát trực tiếp bằng `openpyxl` trên file thật, người
dùng giải thích luồng nghiệp vụ song song. Các sheet thật:
`PA`, `B8 (PA)`, `Tính Q`, `Sheet1`, `Bán2`, `CLB`, `B8`, `PL`, `BK
chứng thư 11 2025`, `B8 (2)`, `THmuaKV` — 2 sheet cuối (`Sheet1`, `BK
chứng thư 11 2025`) **chưa từng có trong tài liệu khảo sát cũ**.

### 9a. `CLB` — chất lượng bán (input, đã xác nhận từ người dùng)

Cột: `Tháng | Cám | Lượng | Ak | Vk | Qk | Sk` — 1 dòng = 1 (tháng,
cám thành phẩm), là **chất lượng bán thực tế** (không phải chất lượng
tính từ PA). **Nhập tay hoặc cập nhật từ file cán bộ Hàng bán cung
cấp** (theo người dùng). Đã xác nhận được nguồn cụ thể: sheet `BK
chứng thư 11 2025` trong cùng file có **số liệu giống hệt** `CLB` (vd
"Cám 5a.10 (ĐTB)" tháng 1: Lượng=167460.6, Ak=29.97, Vk=9.47, Qk=5775,
Sk=0.63 — khớp tuyệt đối cả 2 sheet) → đây chính là bảng kê chứng thư
giám định chất lượng (nguồn "cán bộ Hàng bán cung cấp" mà người dùng
nhắc tới), dùng để cập nhật `CLB`.

### 9b. `Bán2` — đã giải mã các cột từng ghi "chưa xác nhận"

Cấu trúc đúng layout query `Bán`/`tenthan` của `QTTPT_2026.m` (`SPT,
N_HD, N_PT, N_NT, Tram, Data.Column6, Data.Column7, Ak, Vk, Sk, Qk,
STTPA, Cảng, Tháng, L_TTT, L_TTN, L_PA, L_HHB, L_KK, L_XCN, L_NCN,
L_B`), có thêm các cột **`C_TP`/`C_PT`/`PL`/`C_B8`** — đúng những cột
đang ghi "chưa xác nhận ý nghĩa" trong `CLAUDE.md` mục 6 (nguồn từ
sheet `CN` trong `QTTPT 2026.xlsx`). Đã giải mã bằng dữ liệu thật:

- **`PL` = "TN" (Trong Nước) hoặc "NK" (Nhập Khẩu)** — khớp thẳng với
  field `san_pham.nguon_goc` (`trong_nuoc`/`nhap_khau`) đã cài ở
  Module 2. **Đây là câu trả lời cho điểm chưa xác nhận về ý nghĩa cột
  `PL` trong sheet `CN`.**
- `C_TP` = tên sản phẩm đầu ra (trùng giá trị `Data.Column6`).
- `C_PT` = nhãn đầy đủ của thành phần đầu vào, có kèm khoảng thời gian
  hiệu lực Ak khi là than trong nước (vd `"- Cám 5b.1 (Ak
  31,01-35,00) (từ 04/01/2025 đến 19/12/2025)"`).
- `C_B8` = bản rút gọn của `C_PT` (bỏ khoảng thời gian) — dùng làm
  nhãn Biểu 8 cho thành phần đó.
- Thêm 5 cột cuối chưa từng ghi trong tài liệu cũ: **`B_Ak`/`B_Vk`/
  `B_Qk`/`B_Sk`** (giá trị quan sát = 0 ở các dòng có `L_B=0` — gợi ý
  đây là **lượng bán × chỉ tiêu chất lượng** theo từng lô, tử số của
  công thức bình quân gia quyền) và **`Round`** (có vẻ liên quan tới
  cùng cơ chế làm tròn/rank đã ghi ở mục 8) — **CHƯA XÁC NHẬN chính
  xác công thức**, chỉ mới suy luận hợp lý từ cấu trúc, cần hỏi thêm
  khi cần độ chính xác cao.

### 9c. `B8`/`B8 (2)`/`B8 (PA)` — bước hiệu chỉnh chất lượng cấp cho DCCL (đã xác nhận từ người dùng 2026-07-10)

Đây là bước quan trọng nhất của file, **khác hẳn** phép bình quân gia
quyền đơn giản đã cài ở `can_bang_chat.py::binh_quan_gia_quyen()`.
Với mỗi (Tháng, Cám thành phẩm), cấu trúc mỗi sheet `B8`/`B8 (2)`:

- **Dòng 1**: chất lượng mục tiêu (lấy từ `CLB` — chất lượng bán thực
  đo).
- **Dòng 2**: bình quân gia quyền tính từ các dòng PA thành phần, và
  **chênh lệch** giữa dòng 1 và bình quân này — tính với độ chính xác
  cao hơn mức hiển thị cuối (Ak/Vk/Sk lấy 4 số thập phân, Qk lấy 2 số
  — do đơn vị Qk lớn hơn hẳn, cal/g).
- **Dòng 3**: giá trị chênh lệch đã làm tròn đúng mức cần phân bổ.
- **Cột J-M**: nơi phân bổ chênh lệch — **CHỈNH TAY THEO KINH NGHIỆM**
  (xác nhận trực tiếp từ người dùng, không theo công thức/rank cố
  định như quy tắc ở mục 8), tăng dần từng bước nhỏ (**0,01 với
  Ak/Vk/Sk, 1 với Qk**) xuống các dòng cám thành phần (từ dòng 5), cho
  tới khi chênh lệch ở dòng 2 **tiến gần 0 nhất có thể**.
- **Cột A-I, từ dòng 5 trở xuống**: kết quả — chất lượng **đã hiệu
  chỉnh** của từng cám thành phần, đây mới là dữ liệu **cấp cho
  `DCCL`** (không phải chất lượng gốc từ PA).

**Ý nghĩa quan trọng cho thiết kế Module 8** — đây là **bản chất
nghiệp vụ khác hẳn** quy tắc làm tròn phân bổ lượng ở mục 8
(`Append1`): quy tắc đó là **thuật toán xác định** (rank theo delta,
tự động hoá được 100%); bước hiệu chỉnh chất lượng này là **thao tác
thủ công có chủ đích, dựa vào kinh nghiệm người làm**, không nên ép
thành công thức cứng trong CSDL mới — nếu tự động hoá sẽ cho kết quả
khác người làm tay, sai lệch số liệu kế toán. Thiết kế đúng: hệ thống
có thể **gợi ý** bình quân gia quyền ban đầu + hiển thị chênh lệch so
với `CLB`, nhưng **giá trị cuối cùng cấp cho DCCL phải do người dùng
xác nhận/chỉnh tay** — cùng tính chất với `ĐN QÂ` (Module 3) và kết
quả kiểm kê (Module 6), KHÔNG phải giá trị suy ra thuần tuý.
**`can_bang_chat.py` hiện tại CHƯA có bước hiệu chỉnh này** — cần bổ
sung khi làm tiếp Module 8.

Sheet `Tính Q` chứa bảng hệ số quy đổi theo loại than (Ak trung bình,
chênh lệch Ak cho phép, "sự biến thiên nhiệt năng cho 1 đơn vị Ak",
Qk max/min...) — nhiều khả năng dùng để quy đổi chênh lệch Ak thành
chênh lệch Qk tương ứng trong bước hiệu chỉnh trên, nhưng **CHƯA XÁC
NHẬN** công thức chính xác dùng bảng này ở đâu trong `B8`.

Sheet `Sheet1`, `PL`, `THmuaKV` — **CHƯA XÁC NHẬN** vai trò cụ thể.

## 10. `QTTPT 2026.xlsx` và `THP.Biểu mẫu Quyết toán KVCP 2026.xlsx` — đối chiếu bằng file thật (2026-07-10)

Người dùng cung cấp trực tiếp cả 2 file quyết toán còn thiếu. Đã đọc
bằng `openpyxl`, giải quyết dứt điểm các điểm chưa xác nhận liên quan
tới sheet `CN` và `DCCL`.

### 10a. Bảng `CN` thật — cấu trúc đầy đủ, giải mã cơ chế XCN/NCN

Tìm thấy đúng bảng nguồn mà `QTTPT_2026.m` đọc qua
`Excel.CurrentWorkbook(){[Name="CN"]}` — nằm trong **sheet `XCN`** của
`QTTPT 2026.xlsx` (tên sheet và tên bảng Excel khác nhau — mẫu thường
gặp). Cột đầy đủ: `SPT, N_HD, N_PT, N_NT, Tram, Data.Column6,
Data.Column7, L_100, Ak, Vk, Sk, Qk, L_T, STTPA, Cảng, Tháng, C_TP,
C_PT, PL, C_B8, C_CN`.

Ví dụ dòng thật (SPT=5, trạm CC, tháng 1):
```
Data.Column6 (=C_TP) = "5a.10 ĐHP"
Data.Column7          = "Cám 5b.1"
C_PT  = "- Cám 5b.1 (Ak 31,01-35,00) (từ 01/01/2026 đến 05/03/2026)"
C_B8  = "- Cám 5b.1 (Ak 31,01-35,00)"   (= C_PT bỏ khoảng thời gian)
PL    = "TN"
C_CN  = "5a.10 ĐTB"      ← KHÁC C_TP!
L_T   = 3.69
```

**Cơ chế đã giải mã đầy đủ**: đối chiếu với `QTTPT_2026.m` dòng
165-181 (`XCN` bỏ cột `C_CN`, giữ `Data.Column6`/`C_TP` làm sản phẩm
gắn; `NCN` bỏ cột `Data.Column6`, đổi `C_CN` thành `Data.Column6` mới)
— **1 dòng `CN` = 1 giao dịch chuyển nguồn, chuyển `L_T` tấn của 1
thành phần (`Data.Column7`) từ đang được TÍNH VÀO sản phẩm `C_TP`
sang TÍNH VÀO sản phẩm `C_CN`**. Khi tính `L_B` cho `C_TP` (ở đây
"5a.10 ĐHP"), lượng này trừ đi (`−L_XCN`, coi là xuất khỏi 5a.10 ĐHP);
khi tính `L_B` cho `C_CN` (ở đây "5a.10 ĐTB"), lượng này cộng vào
(`+L_NCN`, coi là nhập vào 5a.10 ĐTB). Đúng với ý nghĩa nghiệp vụ đã
xác nhận trực tiếp từ người dùng ở mục 6: XCN/NCN phục vụ việc
**chuyển 1 lô đang tính cho đích bán này sang tính cho đích bán khác**
(ở đây là chuyển từ "5a.10 ĐTB" sang "5a.10 ĐHP" — 2 đích bán khác
nhau của cùng 1 sản phẩm gốc "5a.10").

`STTPA=-1` cũng xuất hiện ở các dòng `CN` này (giống dòng "tồn năm
trước" đã xác nhận ở mục 6) — hợp lý vì dòng chuyển nguồn cũng không
phải 1 PA thật trong năm, dùng chung quy ước cờ âm.

**Kết luận**: đóng điểm "chưa xác nhận cột C_PT/C_B8" ở `CLAUDE.md`
mục 6 — công thức/ý nghĩa đã rõ. Việc còn lại chỉ là code Module 7 đọc
đúng bảng `CN` này (đường dẫn tương tự Module 4 đọc PA — 1 dòng/lô).

### 10b. `DCCL` — xác nhận layout thật + đối chiếu số khớp tuyệt đối với `B8`

Layout thật của `DCCL` (trong `THP.Biểu mẫu Quyết toán KVCP
2026.xlsx`): `Tháng | Thành phẩm | Than pha trộn | (cột trùng tên) |
Lượng | AK | Vk | Qk | Sk` — 1 dòng = 1 (tháng, cám thành phẩm, cám
thành phần cấu thành).

**Đối chiếu số thật, khớp tuyệt đối** — dòng `Tháng=5, Thành phẩm="Cám
6b.1 ĐHD", Than pha trộn="- Cám 5b.3 (Ak 31,01-35)"`: `DCCL` ghi
`Lượng=11901.49, AK=34.17, Vk=4.1, Qk=5110, Sk=0.86`. Đối chiếu với
sheet `B8` của `Cân bằng chất.xlsx` (mục 9c) cùng dòng (`Cám 6b.1
ĐHD`/`- Cám 5b.3`, tháng 5): cột `E5=11901.49` (Lượng, khớp), và
**khối cột R-U** (`S5=34.17, T5=4.1, U5=5110, V5=0.86`) — **khớp
tuyệt đối** với `DCCL`. Đây là bằng chứng số xác định chính xác: `B8`
có NHIỀU khối cột hiệu chỉnh liên tiếp (F-I thô, J-M delta, N-Q hiệu
chỉnh bước 1...), và **khối R-U mới là kết quả CUỐI CÙNG cấp cho
`DCCL`** — không phải khối N-Q như có thể nhầm khi đọc thoáng qua.

**Kết luận**: đóng điểm "CHƯA đối chiếu được với `DCCL` thật" ở
`TASK.md` Phase 7 — nay đã có căn cứ số liệu thật, đủ tin cậy để code
Module 8 theo đúng layout và xác định đúng khối cột cần lấy.

### 10c. `Bán2` (Cân bằng chất.xlsx) so với `Bán` (QTTPT 2026.xlsx thật)

Sheet `Bán` trong `QTTPT 2026.xlsx` có cấu trúc **giống hệt** `Bán2`
của `Cân bằng chất.xlsx` (mục 9b) TRỪ 5 cột cuối `B_Ak/B_Vk/B_Qk/
B_Sk/Round` — xác nhận các cột này **không thuộc đầu ra gốc của
`QTTPT_2026.m`**, mà là cột tính thêm riêng trong `Cân bằng chất.xlsx`
(nhiều khả năng: bản sao của `Bán` được dán qua rồi tính thêm cột phụ
cho mục đích cân bằng chất) — công thức chính xác của 5 cột này
**vẫn CHƯA XÁC NHẬN**, nhưng phạm vi đã thu hẹp (chỉ liên quan tới
`Cân bằng chất.xlsx`, không phải đầu ra chuẩn của Module 7).

### 10d. Sheet `Quyết toán` — xác nhận tồn tại, chưa phân tích layout chi tiết

`QTTPT 2026.xlsx` có sheet `Quyết toán`/`Quyết toán (T)` — văn bản
chính thức "BIÊN BẢN VỀ VIỆC QUYẾT TOÁN GIÁ TRỊ MUA/BÁN THAN PTNK"
theo quý, có căn cứ hợp đồng/công văn cụ thể, cấu trúc rất lớn (873
dòng). **Chưa phân tích chi tiết layout cột** ở đợt khảo sát này (nằm
ngoài phạm vi giai đoạn hiện tại — task yêu cầu "chưa cần lập trình
xuất file", và giá vốn than đã chốt KHÔNG tự động hoá) — để dành khi
thực sự bắt đầu code phần xuất báo cáo Module 7.
