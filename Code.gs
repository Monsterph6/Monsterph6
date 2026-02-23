const SHEET_MEMBERS = 'ThanhVien';
const SHEET_PRAYERS = 'VanKhan';
const MEMBER_HEADERS = [
  'id',
  'hoTen',
  'ngaySinhDuong',
  'ngaySinhAm',
  'ngayMatDuong',
  'ngayMatAm',
  'gioiTinh',
  'idCha',
  'idMe',
  'ghiChu',
];

const PRAYER_HEADERS = ['id', 'tieuDe', 'chuDe', 'noiDung', 'ghiChu'];

function doGet() {
  ensureSchema_();
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Gia phả & Văn khấn')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

function getInitialData() {
  ensureSchema_();
  return {
    members: getMembers(),
    prayers: getPrayers(),
    familyTree: getFamilyTree(),
  };
}

function getMembers() {
  const sheet = getSheet_(SHEET_MEMBERS, MEMBER_HEADERS);
  const rows = readRows_(sheet);
  return rows.map((row) => {
    const ngaySinhDuong = row.ngaySinhDuong || row.ngaySinh || '';
    const ngayMatDuong = row.ngayMatDuong || row.ngayMat || '';

    return {
      id: String(row.id || ''),
      hoTen: row.hoTen || '',
      ngaySinhDuong,
      ngaySinhAm: row.ngaySinhAm || (ngaySinhDuong ? convertDatePair_(ngaySinhDuong, 'duong').am : ''),
      ngayMatDuong,
      ngayMatAm: row.ngayMatAm || (ngayMatDuong ? convertDatePair_(ngayMatDuong, 'duong').am : ''),
      gioiTinh: row.gioiTinh || '',
      idCha: String(row.idCha || ''),
      idMe: String(row.idMe || ''),
      ghiChu: row.ghiChu || '',
    };
  });
}

function getPrayers() {
  const sheet = getSheet_(SHEET_PRAYERS, PRAYER_HEADERS);
  const rows = readRows_(sheet);
  return rows.map((row) => ({
    id: String(row.id || ''),
    tieuDe: row.tieuDe || '',
    chuDe: row.chuDe || '',
    noiDung: row.noiDung || '',
    ghiChu: row.ghiChu || '',
  }));
}

function addMember(payload) {
  ensureSchema_();
  validateRequired_(payload, ['hoTen']);

  const ngaySinh = convertDatePair_(payload.ngaySinhInput || '', payload.ngaySinhLoai || 'duong');
  const ngayMat = convertDatePair_(payload.ngayMatInput || '', payload.ngayMatLoai || 'duong');

  const sheet = getSheet_(SHEET_MEMBERS, MEMBER_HEADERS);
  const id = createId_();
  const row = [
    id,
    payload.hoTen || '',
    ngaySinh.duong,
    ngaySinh.am,
    ngayMat.duong,
    ngayMat.am,
    payload.gioiTinh || '',
    payload.idCha || '',
    payload.idMe || '',
    payload.ghiChu || '',
  ];
  sheet.appendRow(row);

  return { ok: true, id };
}

function addPrayer(payload) {
  ensureSchema_();
  validateRequired_(payload, ['tieuDe', 'noiDung']);

  const sheet = getSheet_(SHEET_PRAYERS, PRAYER_HEADERS);
  const id = createId_();
  const row = [id, payload.tieuDe || '', payload.chuDe || '', payload.noiDung || '', payload.ghiChu || ''];
  sheet.appendRow(row);

  return { ok: true, id };
}

function getFamilyTree() {
  const members = getMembers();
  const byId = {};

  members.forEach((member) => {
    byId[member.id] = { ...member, children: [] };
  });

  const roots = [];
  members.forEach((member) => {
    const node = byId[member.id];
    const parentId = member.idCha || member.idMe;
    if (parentId && byId[parentId]) {
      byId[parentId].children.push(node);
    } else {
      roots.push(node);
    }
  });

  return roots;
}

function ensureSchema_() {
  getSheet_(SHEET_MEMBERS, MEMBER_HEADERS);
  getSheet_(SHEET_PRAYERS, PRAYER_HEADERS);
}

function getSheet_(name, headers) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(name);

  if (!sheet) {
    sheet = ss.insertSheet(name);
  }

  if (headers && headers.length > 0) {
    const lastCol = Math.max(sheet.getLastColumn(), headers.length);
    const existing = sheet.getRange(1, 1, 1, lastCol).getValues()[0].map((cell) => String(cell || ''));
    const isBlank = existing.every((cell) => cell === '');

    if (isBlank) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.setFrozenRows(1);
    } else {
      const existingNonBlank = existing.filter((cell) => cell !== '');
      const canMigrate = existingNonBlank.every((cell) => headers.indexOf(cell) >= 0);
      if (!canMigrate) {
        throw new Error(`Sheet ${name} có header không tương thích. Vui lòng kiểm tra lại cột.`);
      }
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.setFrozenRows(1);
    }
  }

  return sheet;
}

function readRows_(sheet) {
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();

  if (lastRow < 2 || lastCol === 0) {
    return [];
  }

  const header = sheet.getRange(1, 1, 1, lastCol).getValues()[0].map(String);
  const values = sheet.getRange(2, 1, lastRow - 1, lastCol).getValues();

  return values.map((row) => {
    const obj = {};
    header.forEach((key, index) => {
      obj[key] = row[index];
    });
    return obj;
  });
}

function validateRequired_(payload, fields) {
  if (!payload || typeof payload !== 'object') {
    throw new Error('Dữ liệu đầu vào không hợp lệ.');
  }

  fields.forEach((field) => {
    if (!payload[field] || String(payload[field]).trim() === '') {
      throw new Error(`Thiếu trường bắt buộc: ${field}`);
    }
  });
}

function createId_() {
  return Utilities.getUuid();
}

function convertDatePair_(inputDate, inputType) {
  if (!inputDate) {
    return { duong: '', am: '' };
  }

  const type = inputType === 'am' ? 'am' : 'duong';

  if (type === 'duong') {
    const solar = parseInputDate_(inputDate);
    const lunar = convertSolar2Lunar_(solar.dd, solar.mm, solar.yy, 7);
    return {
      duong: formatDate_(solar.dd, solar.mm, solar.yy),
      am: formatDate_(lunar.day, lunar.month, lunar.year),
    };
  }

  const lunar = parseInputDate_(inputDate);
  const solar = convertLunar2Solar_(lunar.dd, lunar.mm, lunar.yy, 0, 7);
  return {
    duong: formatDate_(solar.day, solar.month, solar.year),
    am: formatDate_(lunar.dd, lunar.mm, lunar.yy),
  };
}

function parseInputDate_(value) {
  const str = String(value).trim();
  if (!str) {
    throw new Error('Ngày không hợp lệ.');
  }

  if (/^\d{4}-\d{2}-\d{2}$/.test(str)) {
    const parts = str.split('-').map(Number);
    return { yy: parts[0], mm: parts[1], dd: parts[2] };
  }

  if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(str)) {
    const parts = str.split('/').map(Number);
    return { dd: parts[0], mm: parts[1], yy: parts[2] };
  }

  throw new Error('Định dạng ngày phải là yyyy-mm-dd hoặc dd/mm/yyyy.');
}

function formatDate_(dd, mm, yy) {
  return `${pad2_(dd)}/${pad2_(mm)}/${yy}`;
}

function pad2_(num) {
  return num < 10 ? `0${num}` : String(num);
}

function INT_(d) {
  return Math.floor(d);
}

function jdFromDate_(dd, mm, yy) {
  const a = INT_((14 - mm) / 12);
  const y = yy + 4800 - a;
  const m = mm + 12 * a - 3;
  let jd = dd + INT_((153 * m + 2) / 5) + 365 * y + INT_(y / 4) - INT_(y / 100) + INT_(y / 400) - 32045;
  if (jd < 2299161) {
    jd = dd + INT_((153 * m + 2) / 5) + 365 * y + INT_(y / 4) - 32083;
  }
  return jd;
}

function jdToDate_(jd) {
  let a;
  let b;
  let c;

  if (jd > 2299160) {
    a = jd + 32044;
    b = INT_((4 * a + 3) / 146097);
    c = a - INT_((b * 146097) / 4);
  } else {
    b = 0;
    c = jd + 32082;
  }

  const d = INT_((4 * c + 3) / 1461);
  const e = c - INT_((1461 * d) / 4);
  const m = INT_((5 * e + 2) / 153);
  const day = e - INT_((153 * m + 2) / 5) + 1;
  const month = m + 3 - 12 * INT_(m / 10);
  const year = b * 100 + d - 4800 + INT_(m / 10);

  return { day, month, year };
}

function getNewMoonDay_(k, timeZone) {
  const T = k / 1236.85;
  const T2 = T * T;
  const T3 = T2 * T;
  const dr = Math.PI / 180;
  let Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3;
  Jd1 += 0.00033 * Math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr);
  const M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3;
  const Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3;
  const F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3;
  let C1 = (0.1734 - 0.000393 * T) * Math.sin(M * dr) + 0.0021 * Math.sin(2 * dr * M);
  C1 -= 0.4068 * Math.sin(Mpr * dr) + 0.0161 * Math.sin(dr * 2 * Mpr);
  C1 -= 0.0004 * Math.sin(dr * 3 * Mpr);
  C1 += 0.0104 * Math.sin(dr * 2 * F) - 0.0051 * Math.sin(dr * (M + Mpr));
  C1 -= 0.0074 * Math.sin(dr * (M - Mpr)) + 0.0004 * Math.sin(dr * (2 * F + M));
  C1 -= 0.0004 * Math.sin(dr * (2 * F - M)) - 0.0006 * Math.sin(dr * (2 * F + Mpr));
  C1 += 0.001 * Math.sin(dr * (2 * F - Mpr)) + 0.0005 * Math.sin(dr * (2 * Mpr + M));
  let deltat;
  if (T < -11) {
    deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3;
  } else {
    deltat = -0.000278 + 0.000265 * T + 0.000262 * T2;
  }
  const JdNew = Jd1 + C1 - deltat;
  return INT_(JdNew + 0.5 + timeZone / 24);
}

function getSunLongitude_(jdn, timeZone) {
  const T = (jdn - 2451545.5 - timeZone / 24) / 36525;
  const T2 = T * T;
  const dr = Math.PI / 180;
  const M = 357.5291 + 35999.0503 * T - 0.0001559 * T2 - 0.00000048 * T * T2;
  const L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2;
  let DL = (1.9146 - 0.004817 * T - 0.000014 * T2) * Math.sin(dr * M);
  DL += (0.019993 - 0.000101 * T) * Math.sin(dr * 2 * M) + 0.00029 * Math.sin(dr * 3 * M);
  const L = L0 + DL;
  const omega = L * dr;
  return INT_((omega / Math.PI) * 6);
}

function getLunarMonth11_(yy, timeZone) {
  const off = jdFromDate_(31, 12, yy) - 2415021;
  const k = INT_(off / 29.530588853);
  let nm = getNewMoonDay_(k, timeZone);
  const sunLong = getSunLongitude_(nm, timeZone);
  if (sunLong >= 9) {
    nm = getNewMoonDay_(k - 1, timeZone);
  }
  return nm;
}

function getLeapMonthOffset_(a11, timeZone) {
  const k = INT_(0.5 + (a11 - 2415021.076998695) / 29.530588853);
  let last = 0;
  let i = 1;
  let arc = getSunLongitude_(getNewMoonDay_(k + i, timeZone), timeZone);
  do {
    last = arc;
    i += 1;
    arc = getSunLongitude_(getNewMoonDay_(k + i, timeZone), timeZone);
  } while (arc !== last && i < 14);
  return i - 1;
}

function convertSolar2Lunar_(dd, mm, yy, timeZone) {
  const dayNumber = jdFromDate_(dd, mm, yy);
  const k = INT_((dayNumber - 2415021.076998695) / 29.530588853);
  let monthStart = getNewMoonDay_(k + 1, timeZone);
  if (monthStart > dayNumber) {
    monthStart = getNewMoonDay_(k, timeZone);
  }

  let a11 = getLunarMonth11_(yy, timeZone);
  let b11 = a11;
  let lunarYear;

  if (a11 >= monthStart) {
    lunarYear = yy;
    a11 = getLunarMonth11_(yy - 1, timeZone);
  } else {
    lunarYear = yy + 1;
    b11 = getLunarMonth11_(yy + 1, timeZone);
  }

  const lunarDay = dayNumber - monthStart + 1;
  const diff = INT_((monthStart - a11) / 29);
  let lunarMonth = diff + 11;
  let lunarLeap = 0;

  if (b11 - a11 > 365) {
    const leapMonthDiff = getLeapMonthOffset_(a11, timeZone);
    if (diff >= leapMonthDiff) {
      lunarMonth = diff + 10;
      if (diff === leapMonthDiff) {
        lunarLeap = 1;
      }
    }
  }

  if (lunarMonth > 12) {
    lunarMonth -= 12;
  }
  if (lunarMonth >= 11 && diff < 4) {
    lunarYear -= 1;
  }

  return { day: lunarDay, month: lunarMonth, year: lunarYear, leap: lunarLeap };
}

function convertLunar2Solar_(lunarDay, lunarMonth, lunarYear, lunarLeap, timeZone) {
  let a11;
  let b11;

  if (lunarMonth < 11) {
    a11 = getLunarMonth11_(lunarYear - 1, timeZone);
    b11 = getLunarMonth11_(lunarYear, timeZone);
  } else {
    a11 = getLunarMonth11_(lunarYear, timeZone);
    b11 = getLunarMonth11_(lunarYear + 1, timeZone);
  }

  const off = lunarMonth - 11 < 0 ? lunarMonth - 11 + 12 : lunarMonth - 11;
  let k = INT_(0.5 + (a11 - 2415021.076998695) / 29.530588853);
  let offset = off;

  if (b11 - a11 > 365) {
    const leapOff = getLeapMonthOffset_(a11, timeZone);
    let leapMonth = leapOff - 2;
    if (leapMonth < 0) {
      leapMonth += 12;
    }

    if (lunarLeap !== 0 && lunarMonth !== leapMonth) {
      throw new Error('Ngày âm không hợp lệ (tháng nhuận).');
    }

    if (lunarLeap !== 0 || off >= leapOff) {
      offset += 1;
    }
  }

  const monthStart = getNewMoonDay_(k + offset, timeZone);
  return jdToDate_(monthStart + lunarDay - 1);
}
