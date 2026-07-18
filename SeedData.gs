/**
 * Dữ liệu gốc trích từ file "Phả đồ chi họ Phạm Hiếu" (Excel).
 * Được dùng để khởi tạo Google Sheet lần đầu tiên chạy app.
 *
 * Cấu trúc mỗi dòng:
 * [ID, HoTen, GioiTinh, Doi, ChaID, VoChongCuaID, NgayGio, NamSinh, NamMat, ChucDanh, GhiChu, ThuTu]
 *
 * - ChaID        : ID của người cha/mẹ trong họ (quan hệ huyết thống).
 * - VoChongCuaID : nếu là vợ/chồng (dâu, rể) thì ghi ID của người phối ngẫu trong họ.
 * - NgayGio      : ngày giỗ âm lịch, dạng "ngày/tháng" (vd "18/12").
 * - ThuTu        : thứ tự anh chị em trong cùng một gia đình.
 */

var GIAPHA_TITLE = 'PHẢ ĐỒ CHI HỌ PHẠM HIẾU LÀNG LIỄU ĐIỆN XÃ CAO MINH HUYỆN VĨNH BẢO';

var SEED_HEADERS = ['ID', 'HoTen', 'GioiTinh', 'Doi', 'ChaID', 'VoChongCuaID', 'NgayGio', 'NamSinh', 'NamMat', 'ChucDanh', 'GhiChu', 'ThuTu'];

var SEED_DATA = [
  // ----- Đời 1: TIÊN TỔ -----
  [1,  'Phạm Hiếu Tiết',  'Nam', 1, '',  '',  '18/12', '', '', 'Tiên tổ', '', 1],
  [2,  'Phạm Thị Quang',  'Nữ',  1, '',  1,   '9/9',   '', '', '', 'Vợ cụ Phạm Hiếu Tiết', 1],

  // ----- Đời 2: CAO TỔ -----
  [3,  'Phạm Hiếu Kính',  'Nam', 2, 1,   '',  '8/6',   '', '', 'Cao tổ — Nhánh 1', '', 1],
  [4,  'Phạm Thị Sáng',   'Nữ',  2, '',  3,   '8/4',   '', '', '', 'Vợ cụ Phạm Hiếu Kính', 1],
  [5,  'Phạm Hiếu Chân',  'Nam', 2, 1,   '',  '4/2',   '', '', 'Cao tổ — Nhánh 2', '', 2],
  [6,  'Phạm Thị Tần',    'Nữ',  2, '',  5,   '',      '', '', '', 'Vợ cụ Phạm Hiếu Chân', 1],

  // ----- Đời 3: TẰNG TỔ (con cụ Phạm Hiếu Chân) -----
  [7,  'Phạm Trung Hiền', 'Nam', 3, 5,   '',  '3/2',   '', '', 'Tằng tổ', '', 1],
  [8,  'Phạm Thị Linh',   'Nữ',  3, '',  7,   '1/2',   '', '', '', 'Vợ cụ Phạm Trung Hiền', 1],

  // ----- Đời 4: HIỀN TỔ (con cụ Phạm Trung Hiền) -----
  [10, 'Phạm Hiếu Điều',  'Nam', 4, 7,   '',  '12/4',  '', '', 'Hiền tổ — Ngành trưởng', '', 1],
  [11, 'Phạm Thị Chậm',   'Nữ',  4, '',  10,  '1/6',   '', '', '', 'Vợ cụ Phạm Hiếu Điều', 1],
  [12, 'Phạm Thị Chỉ',    'Nữ',  4, '',  10,  '',      '', '', '', 'Vợ cụ Phạm Hiếu Điều', 2],
  [9,  'Phạm Hiếu Hòa',   'Nam', 4, 7,   '',  '',      '', '', 'Hiền tổ — Ngành thứ hai', 'Chắt cúng', 2],
  [13, 'Phạm Hiếu Quý',   'Nam', 4, 7,   '',  '',      '', '', 'Hiền tổ — Ngành thứ ba', 'Nuôi cúng', 3],

  // ----- Đời 5: THẾ HỆ THỨ NĂM (con cụ Phạm Hiếu Điều) -----
  [14, 'Phạm Hiếu Luật',  'Nam', 5, 10,  '',  '',      '', '', 'Chi trưởng', '', 1],
  [15, 'Phạm Hiếu Toan',  'Nam', 5, 10,  '',  '',      '', '', 'Chi thứ hai', '', 2],
  [16, 'Phạm Hiếu Tuyên', 'Nam', 5, 10,  '',  '',      '', '', 'Chi thứ ba', '', 3],
  [17, 'Phạm Thị Cún',    'Nữ',  5, '',  16,  '',      '', '', '', 'Vợ cụ Phạm Hiếu Tuyên', 1],
  [18, 'Phạm Thị Roan',   'Nữ',  5, 10,  '',  '',      '', '', 'Tổ cô', '', 4],

  // ----- Đời 6: THẾ HỆ THỨ SÁU -----
  // Con cụ Phạm Hiếu Luật
  [19, 'Phạm Hiếu Tạo',   'Nam', 6, 14,  '',  '12/8',  '', '', '', '', 1],
  [20, 'Phạm Thị Nhớn',   'Nữ',  6, '',  19,  '',      '', '', '', 'Vợ cụ Phạm Hiếu Tạo', 1],
  // Con cụ Phạm Hiếu Toan
  [21, 'Phạm Hiếu Huyến', 'Nam', 6, 15,  '',  '',      '', '', '', '', 1],
  [22, 'Phạm Hiếu Toản',  'Nam', 6, 15,  '',  '',      '', '', '', '', 2],
  // Con cụ Phạm Hiếu Tuyên
  [23, 'Phạm Hiếu Xá',    'Nam', 6, 16,  '',  '',      '', '', '', '', 1],
  [24, 'Phạm Hiếu Sướng', 'Nam', 6, 16,  '',  '',      '', '', '', '', 2],
  [25, 'Cụ bà (mẹ cụ Cộng, cụ Cư)', 'Nữ', 6, 16, '', '', '', '', '', 'Tên húy chưa rõ — phả đồ ghi "Mẹ cụ Cộng, cụ Cư"', 3],

  // ----- Đời 7: THẾ HỆ THỨ BẢY -----
  // Con cụ Phạm Hiếu Tạo
  [26, 'Phạm Hiếu Tu',    'Nam', 7, 19,  '',  '',      '', '', '', '', 1],
  [27, 'Phạm Hiếu Chí',   'Nam', 7, 19,  '',  '',      '', '', '', '', 2],
  [28, 'Phạm Thị Úc',     'Nữ',  7, 19,  '',  '',      '', '', '', '', 3],
  [29, 'Phạm Thị Nuôi',   'Nữ',  7, 19,  '',  '',      '', '', '', '', 4],
  // Con cụ Phạm Hiếu Huyến
  [30, 'Phạm Hiếu Điến',  'Nam', 7, 21,  '',  '',      '', '', '', '', 1],
  [31, 'Phạm Hiếu Cáp',   'Nam', 7, 21,  '',  '',      '', '', '', '', 2],
  // Con cụ Phạm Hiếu Toản
  [32, 'Phạm Hiếu Tám',   'Nam', 7, 22,  '',  '',      '', '', '', '', 1],
  [33, 'Phạm Thị Soạn',   'Nữ',  7, 22,  '',  '',      '', '', '', '', 2],
  // Con cụ Phạm Hiếu Xá
  [34, 'Phạm Hiếu Múc',   'Nam', 7, 23,  '',  '',      '', '', '', '', 1],
  [35, 'Phạm Hiếu Míc',   'Nam', 7, 23,  '',  '',      '', '', '', '', 2],
  [36, 'Phạm Thị Rễ',     'Nữ',  7, 23,  '',  '',      '', '', '', '', 3],
  [37, 'Phạm Thị Rãi',    'Nữ',  7, 23,  '',  '',      '', '', '', '', 4],
  [38, 'Phạm Trung Dũng', 'Nam', 7, 23,  '',  '',      '', '', '', '', 5],
  [39, 'Vũ Thị Nhớn',     'Nữ',  7, '',  38,  '',      '', '', '', 'Vợ cụ Phạm Trung Dũng', 1],
  [40, 'Trần Thị Rĩnh',   'Nữ',  7, '',  38,  '',      '', '', '', 'Vợ cụ Phạm Trung Dũng', 2],
  [41, 'Phạm Thị Gái',    'Nữ',  7, 23,  '',  '',      '', '', '', '', 6],
  [42, 'Vũ Bá Tăng',      'Nam', 7, '',  41,  '',      '', '', '', 'Chồng cụ Phạm Thị Gái', 1],
  [43, 'Phạm Thao Lược',  'Nam', 7, 23,  '',  '',      '', '', '', '', 7],
  [44, 'Phạm Thị Thu',    'Nữ',  7, 23,  '',  '',      '', '', '', 'Vị trí trên phả đồ cạnh cụ Thao Lược — cần xác minh', 8],
  // Con cụ Phạm Hiếu Sướng
  [45, 'Phạm Hiếu Ca',    'Nam', 7, 24,  '',  '',      '', '', '', '', 1],
  [46, 'Phạm Hiếu Tiễu',  'Nam', 7, 24,  '',  '',      '', '', '', '', 2],
  [47, 'Phạm Hiếu Tửu',   'Nam', 7, 24,  '',  '',      '', '', '', '', 3],
  [48, 'Phạm Thị Hiên',   'Nữ',  7, '',  47,  '',      '', '', '', 'Đứng cùng ô với cụ Tửu trên phả đồ — cần xác minh vợ hay con', 1],
  [49, 'Trần Thị Cảnh',   'Nữ',  7, '',  47,  '',      '', '', '', 'Vợ cụ Phạm Hiếu Tửu', 2],
  [50, 'Phạm Thị Huệ',    'Nữ',  7, 24,  '',  '',      '', '', '', '', 4],
  [51, 'Phạm Thị Mầm',    'Nữ',  7, 24,  '',  '',      '', '', '', '', 5],
  [52, 'Mầm con',         '',    7, 24,  '',  '',      '', '', '', 'Phả đồ ghi "Mầm con" — cần xác minh (có thể là con cụ Mầm)', 6],
  [53, 'Phạm Sinh Huy',   'Nam', 7, 24,  '',  '',      '', '', '', '', 7],
  [54, 'Phạm Thị Hằng',   'Nữ',  7, '',  53,  '',      '', '', '', 'Đứng cùng ô với cụ Huy trên phả đồ — cần xác minh vợ hay con', 1],
  [55, 'Đào Thị Miến',    'Nữ',  7, '',  53,  '',      '', '', '', 'Vợ cụ Phạm Sinh Huy', 2],
  // Con cụ bà (mẹ cụ Cộng, cụ Cư)
  [56, 'Phạm Đăng Cộng',  'Nam', 7, 25,  '',  '',      '', '', '', '', 1],
  [57, 'Phạm Đăng Cư',    'Nam', 7, 25,  '',  '',      '', '', '', '', 2],
  [58, 'Phạm Thị Ẩm',     'Nữ',  7, 25,  '',  '',      '', '', '', '', 3]
];
