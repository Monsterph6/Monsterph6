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
  (chỉ chỉnh tiền, không liên quan lượng) vốn dĩ **không có** cột này,
  đây là thiết kế đúng của dữ liệu nguồn, không phải thiếu sót cần
  người dùng bổ sung — quan trọng khi thiết kế gate nhập liệu (không
  được coi "thiếu ĐN QÂ" luôn luôn = "cần chặn lại chờ nhập tay").
- Nguồn dữ liệu **tự động** cho "ĐN QÂ" (không phải công thức dùng nó)
  **vẫn chưa xác định** — người dùng vẫn điền tay.

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

→ **Ý nghĩa cho thiết kế CSDL**: đây là lý do cụ thể để **không** áp
dụng tuyệt đối nguyên tắc "không lưu cứng số liệu suy ra được" — xem
nguyên tắc #2 đã sửa lại trong `CLAUDE.md` mục 2. Bảng phân bổ theo lô
này nên là 1 bảng snapshot lưu theo kỳ, có cờ đã chốt, không phải view
tính động.
