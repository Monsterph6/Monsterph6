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

/** Điểm vào của web app. */
function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Gia phả — Chi họ Phạm Hiếu')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/** Lấy (hoặc tạo lần đầu) spreadsheet chứa dữ liệu. */
function getSpreadsheet_() {
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
    seedSheet_(sheet);
  }
  return sheet;
}

/** Đổ dữ liệu gốc vào một sheet trống. */
function seedSheet_(sheet) {
  sheet.clear();
  sheet.getRange(1, 1, 1, SEED_HEADERS.length).setValues([SEED_HEADERS])
    .setFontWeight('bold').setBackground('#7b1e1e').setFontColor('#ffffff');
  if (SEED_DATA.length) {
    sheet.getRange(2, 1, SEED_DATA.length, SEED_HEADERS.length).setValues(SEED_DATA);
  }
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, SEED_HEADERS.length);
}

/** Đọc toàn bộ dữ liệu — trả về cho giao diện. */
function getFamilyData() {
  var sheet = getSheet_();
  var values = sheet.getDataRange().getValues();
  var headers = values.shift() || [];
  var persons = values
    .filter(function (row) { return row[0] !== '' && row[0] !== null; })
    .map(function (row) {
      var p = {};
      headers.forEach(function (h, i) { p[h] = row[i]; });
      return p;
    });
  return {
    title: GIAPHA_TITLE,
    sheetUrl: getSpreadsheet_().getUrl(),
    persons: persons
  };
}

/**
 * Thêm hoặc cập nhật một thành viên.
 * person = {ID?, HoTen, GioiTinh, Doi, ChaID, VoChongCuaID, NgayGio, NamSinh, NamMat, ChucDanh, GhiChu, ThuTu}
 * ID rỗng => thêm mới (tự cấp ID). Trả về getFamilyData() sau khi lưu.
 */
function savePerson(person) {
  if (!person || !String(person.HoTen || '').trim()) {
    throw new Error('Họ tên không được để trống.');
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
      sheet.appendRow(row);
    } else {
      sheet.getRange(rowIndex, 1, 1, headers.length).setValues([row]);
    }
    return getFamilyData();
  } finally {
    lock.releaseLock();
  }
}

/** Xóa một thành viên (chặn xóa nếu còn con cháu hoặc vợ/chồng gắn với người này). */
function deletePerson(id) {
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
        throw new Error('Không thể xóa: còn con cháu hoặc vợ/chồng đang gắn với người này. Hãy xóa hoặc chuyển họ trước.');
      }
    }
    for (var r2 = 1; r2 < values.length; r2++) {
      if (Number(values[r2][idCol]) === id) {
        sheet.deleteRow(r2 + 1);
        return getFamilyData();
      }
    }
    throw new Error('Không tìm thấy ID ' + id + '.');
  } finally {
    lock.releaseLock();
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
