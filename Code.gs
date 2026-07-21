/**
 * APP GIA PHẢ — CHI HỌ PHẠM HIẾU
 * Web app chạy trên Google Apps Script, dữ liệu lưu trong Google Sheet.
 *
 * Lần chạy đầu tiên app tự tạo một Google Spreadsheet tên
 * "Dữ liệu Gia phả — Chi họ Phạm Hiếu" và đổ dữ liệu gốc (SeedData.gs) vào.
 * Sau đó mọi thao tác thêm / sửa / xóa đều đọc-ghi trực tiếp trên Sheet này,
 * và cũng có thể mở Sheet để sửa tay.
 */

var SHEET_NAME = 'GiaPha';
var PROP_SS_ID = 'GIAPHA_SPREADSHEET_ID';

/**
 * ID của Google Sheet dùng làm cơ sở dữ liệu.
 * Nếu để trống (''), app sẽ tự tạo một Spreadsheet mới trong Drive khi chạy lần đầu.
 */
var SPREADSHEET_ID = '';

/** Điểm vào của web app. */
function doGet(e) {
  if (e && e.parameter && e.parameter.diag === '1') {
    return ContentService.createTextOutput(JSON.stringify(diagNgayGio_(), null, 2))
      .setMimeType(ContentService.MimeType.JSON);
  }
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Gia phả — Chi họ Phạm Hiếu')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * CHẨN ĐOÁN — liệt kê các ô NgayGio đang bị Sheets tự nhận dạng thành kiểu
 * ngày tháng và có nguy cơ bị đảo ngày/tháng (cả 2 số đều ≤ 12, ví dụ 2/5).
 * Truy cập bằng cách thêm ?diag=1 vào cuối URL web app.
 */
function diagNgayGio_() {
  var sheet = getSheet_();
  var values = sheet.getDataRange().getValues();
  var headers = values[0];
  var idCol = headers.indexOf('ID');
  var nameCol = headers.indexOf('HoTen');
  var gioCol = headers.indexOf('NgayGio');
  var tz = Session.getScriptTimeZone();
  var suspect = [];
  var allDates = [];
  for (var r = 1; r < values.length; r++) {
    var v = values[r][gioCol];
    if (!(v instanceof Date)) continue;
    var d = v.getDate(), m = v.getMonth() + 1;
    var info = { id: values[r][idCol], ten: values[r][nameCol], formatted_ddMM: Utilities.formatDate(v, tz, 'dd/MM') };
    allDates.push(info);
    if (d <= 12 && m <= 12) suspect.push(info); // cả 2 số ≤12 -> có thể đã bị Sheets đảo ngày/tháng
  }
  return { timeZone: tz, tongSoONgayKieuDate: allDates.length, canhBao_coTheBiDaoNgayThang: suspect };
}

/** Lấy (hoặc tạo lần đầu) spreadsheet chứa dữ liệu. */
function getSpreadsheet_() {
  if (SPREADSHEET_ID) {
    return SpreadsheetApp.openById(SPREADSHEET_ID);
  }
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty(PROP_SS_ID);
  if (id) {
    try {
      return SpreadsheetApp.openById(id);
    } catch (e) {
      // Sheet đã bị xóa — tạo lại bên dưới.
    }
  }
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    id = props.getProperty(PROP_SS_ID);
    if (id) {
      try { return SpreadsheetApp.openById(id); } catch (e) {}
    }
    var ss = SpreadsheetApp.create('Dữ liệu Gia phả — Chi họ Phạm Hiếu');
    var sheet = ss.getActiveSheet().setName(SHEET_NAME);
    seedSheet_(sheet);
    props.setProperty(PROP_SS_ID, ss.getId());
    return ss;
  } finally {
    lock.releaseLock();
  }
}

function getSheet_() {
  var ss = getSpreadsheet_();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  // Sheet mới hoặc còn trống -> đổ dữ liệu gốc từ phả đồ vào.
  if (sheet.getLastRow() === 0) {
    seedSheet_(sheet);
  }
  return sheet;
}

/**
 * Các cột phải giữ nguyên dạng chữ (Plain text) — nếu không, Google Sheets sẽ tự nhận
 * dạng "2/5" hay "12/8" là kiểu ngày tháng, và với cặp số đều ≤12 có thể tự đảo
 * ngược ngày/tháng theo locale của Sheet, làm sai hẳn ngày giỗ/năm sinh/năm mất.
 */
var TEXT_COLUMNS = ['NgayGio', 'NamSinh', 'NamMat'];

/** Ép định dạng chữ cho các cột ngày trong vùng dòng chỉ định. */
function forceTextFormat_(sheet, headers, startRow, numRows) {
  TEXT_COLUMNS.forEach(function (name) {
    var col = headers.indexOf(name) + 1;
    if (col > 0 && numRows > 0) {
      sheet.getRange(startRow, col, numRows, 1).setNumberFormat('@');
    }
  });
}

/** Đổ dữ liệu gốc vào một sheet trống. */
function seedSheet_(sheet) {
  sheet.clear();
  sheet.getRange(1, 1, 1, SEED_HEADERS.length).setValues([SEED_HEADERS])
    .setFontWeight('bold').setBackground('#7b1e1e').setFontColor('#ffffff');
  // Ép định dạng chữ TRƯỚC khi ghi dữ liệu, phủ luôn các dòng sẽ thêm tay sau này.
  forceTextFormat_(sheet, SEED_HEADERS, 2, Math.max(sheet.getMaxRows() - 1, SEED_DATA.length));
  if (SEED_DATA.length) {
    sheet.getRange(2, 1, SEED_DATA.length, SEED_HEADERS.length).setValues(SEED_DATA);
  }
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, SEED_HEADERS.length);
}

/** Chuyển các giá trị không phải string/number/boolean (vd Date do Sheets tự nhận dạng) thành chuỗi an toàn cho google.script.run. */
function sanitizeCell_(v) {
  if (v instanceof Date) return Utilities.formatDate(v, Session.getScriptTimeZone() || 'Asia/Ho_Chi_Minh', 'dd/MM');
  if (v === null || v === undefined) return '';
  return v;
}

function pad2_(n) { n = String(n); return n.length < 2 ? '0' + n : n; }

/** Chuẩn hoá ngày giỗ về đúng định dạng dd/MM (có số 0 đứng trước), dù ô là Date hay chữ "d/m". */
function normalizeNgayGio_(v) {
  if (v instanceof Date) return Utilities.formatDate(v, Session.getScriptTimeZone() || 'Asia/Ho_Chi_Minh', 'dd/MM');
  var s = String(v == null ? '' : v).trim();
  var m = s.match(/^(\d{1,2})\s*[\/\-]\s*(\d{1,2})$/);
  if (m) return pad2_(m[1]) + '/' + pad2_(m[2]);
  return s;
}

/** Đọc toàn bộ dữ liệu — trả về cho giao diện. */
function getFamilyData() {
  try {
    var ss = getSpreadsheet_();
    var sheet = getSheet_();
    var values = sheet.getDataRange().getValues();
    var headers = values.shift() || [];
    var persons = values
      .filter(function (row) { return row[0] !== '' && row[0] !== null; })
      .map(function (row) {
        var p = {};
        headers.forEach(function (h, i) {
          p[h] = (h === 'NgayGio') ? normalizeNgayGio_(row[i]) : sanitizeCell_(row[i]);
        });
        return p;
      });
    return {
      title: GIAPHA_TITLE,
      sheetUrl: ss.getUrl(),
      persons: persons
    };
  } catch (e) {
    return { error: true, message: 'Lỗi server: ' + (e && e.message ? e.message : String(e)) };
  }
}

/**
 * Thêm hoặc cập nhật một thành viên.
 * person = {ID?, HoTen, GioiTinh, Doi, ChaID, VoChongCuaID, NgayGio, NamSinh, NamMat, ChucDanh, GhiChu, ThuTu}
 * ID rỗng => thêm mới (tự cấp ID). Trả về getFamilyData() sau khi lưu.
 */
function savePerson(person) {
  try {
    if (!person || !String(person.HoTen || '').trim()) {
      return { error: true, message: 'Họ tên không được để trống.' };
    }
    var lock = LockService.getScriptLock();
    lock.waitLock(30000);
    try {
      var sheet = getSheet_();
      var values = sheet.getDataRange().getValues();
      var headers = values[0];
      var idCol = headers.indexOf('ID');

      var id = person.ID ? Number(person.ID) : 0;
      var rowIndex = -1; // chỉ số dòng (1-based) trong sheet
      var maxId = 0;
      for (var r = 1; r < values.length; r++) {
        var rid = Number(values[r][idCol]);
        if (rid > maxId) maxId = rid;
        if (id && rid === id) rowIndex = r + 1;
      }
      if (!id) {
        id = maxId + 1;
        person.ID = id;
      }
      var row = headers.map(function (h) {
        var v = person[h];
        return v === undefined || v === null ? '' : v;
      });
      if (rowIndex === -1) {
        rowIndex = values.length + 1;
      }
      // Ép định dạng chữ cho dòng này TRƯỚC khi ghi, tránh Sheets tự đổi ngày thành kiểu Date.
      forceTextFormat_(sheet, headers, rowIndex, 1);
      sheet.getRange(rowIndex, 1, 1, headers.length).setValues([row]);
      return getFamilyData();
    } finally {
      lock.releaseLock();
    }
  } catch (e) {
    return { error: true, message: 'Lỗi khi lưu: ' + (e && e.message ? e.message : String(e)) };
  }
}

/** Xóa một thành viên (chặn xóa nếu còn con cháu hoặc vợ/chồng gắn với người này). */
function deletePerson(id) {
  try {
    id = Number(id);
    var lock = LockService.getScriptLock();
    lock.waitLock(30000);
    try {
      var sheet = getSheet_();
      var values = sheet.getDataRange().getValues();
      var headers = values[0];
      var idCol = headers.indexOf('ID');
      var chaCol = headers.indexOf('ChaID');
      var vcCol = headers.indexOf('VoChongCuaID');

      for (var r = 1; r < values.length; r++) {
        if (Number(values[r][chaCol]) === id || Number(values[r][vcCol]) === id) {
          return { error: true, message: 'Không thể xóa: còn con cháu hoặc vợ/chồng đang gắn với người này. Hãy xóa hoặc chuyển họ trước.' };
        }
      }
      for (var r2 = 1; r2 < values.length; r2++) {
        if (Number(values[r2][idCol]) === id) {
          sheet.deleteRow(r2 + 1);
          return getFamilyData();
        }
      }
      return { error: true, message: 'Không tìm thấy ID ' + id + '.' };
    } finally {
      lock.releaseLock();
    }
  } catch (e) {
    return { error: true, message: 'Lỗi khi xóa: ' + (e && e.message ? e.message : String(e)) };
  }
}

/** Khôi phục lại dữ liệu gốc từ phả đồ Excel (ghi đè toàn bộ Sheet). */
function resetToSeed() {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    seedSheet_(getSheet_());
    return getFamilyData();
  } finally {
    lock.releaseLock();
  }
}
