/**
 * Chuyển đổi Dương lịch ↔ Âm lịch Việt Nam.
 * Thuật toán thiên văn chuẩn (dựa trên công thức của Hồ Ngọc Đức, dùng phổ biến
 * cho lịch âm Việt Nam), múi giờ cố định UTC+7. Đã kiểm chứng khớp các mốc
 * Tết Nguyên Đán 2022–2026 trước khi đưa vào dùng.
 */
var VN_TZ_OFFSET = 7;

function jdFromDate_(dd, mm, yy) {
  var a = Math.floor((14 - mm) / 12);
  var y = yy + 4800 - a;
  var m = mm + 12 * a - 3;
  var jd = dd + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
  if (jd < 2299161) {
    jd = dd + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - 32083;
  }
  return jd;
}

function jdToDate_(jd) {
  var a, b, c;
  if (jd > 2299160) {
    a = jd + 32044;
    b = Math.floor((4 * a + 3) / 146097);
    c = a - Math.floor((b * 146097) / 4);
  } else {
    b = 0;
    c = jd + 32082;
  }
  var d = Math.floor((4 * c + 3) / 1461);
  var e = c - Math.floor((1461 * d) / 4);
  var m = Math.floor((5 * e + 2) / 153);
  var day = e - Math.floor((153 * m + 2) / 5) + 1;
  var month = m + 3 - 12 * Math.floor(m / 10);
  var year = b * 100 + d - 4800 + Math.floor(m / 10);
  return [day, month, year];
}

function newMoon_(k) {
  var T = k / 1236.85, T2 = T * T, T3 = T2 * T, dr = Math.PI / 180;
  var Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3;
  Jd1 += 0.00033 * Math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr);
  var M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3;
  var Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3;
  var F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3;
  var C1 = (0.1734 - 0.000393 * T) * Math.sin(M * dr) + 0.0021 * Math.sin(2 * dr * M);
  C1 = C1 - 0.4068 * Math.sin(Mpr * dr) + 0.0161 * Math.sin(dr * 2 * Mpr);
  C1 = C1 - 0.0004 * Math.sin(dr * 3 * Mpr);
  C1 = C1 + 0.0104 * Math.sin(dr * 2 * F) - 0.0051 * Math.sin(dr * (M + Mpr));
  C1 = C1 - 0.0074 * Math.sin(dr * (M - Mpr)) + 0.0004 * Math.sin(dr * (2 * F + M));
  C1 = C1 - 0.0004 * Math.sin(dr * (2 * F - M)) - 0.0006 * Math.sin(dr * (2 * F + Mpr));
  C1 = C1 + 0.0010 * Math.sin(dr * (2 * F - Mpr)) + 0.0005 * Math.sin(dr * (2 * Mpr + M));
  var deltat = (T < -11)
    ? 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    : -0.000278 + 0.000265 * T + 0.000262 * T2;
  return Jd1 + C1 - deltat;
}

function sunLongitude_(jdn, timeZone) {
  var T = (jdn - 2451545.5 - timeZone / 24) / 36525, T2 = T * T, dr = Math.PI / 180;
  var M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2;
  var L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2;
  var DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * Math.sin(dr * M);
  DL = DL + (0.019993 - 0.000101 * T) * Math.sin(dr * 2 * M) + 0.000290 * Math.sin(dr * 3 * M);
  var L = (L0 + DL) * dr;
  L -= Math.PI * 2 * Math.floor(L / (Math.PI * 2));
  return Math.floor(L / Math.PI * 6);
}

function newMoonDay_(k, timeZone) {
  return Math.floor(newMoon_(k) + 0.5 + timeZone / 24);
}

function lunarMonth11_(yy, timeZone) {
  var off = jdFromDate_(31, 12, yy) - 2415021;
  var k = Math.floor(off / 29.530588853);
  var nm = newMoonDay_(k, timeZone);
  if (sunLongitude_(nm, timeZone) >= 9) nm = newMoonDay_(k - 1, timeZone);
  return nm;
}

function leapMonthOffset_(a11, timeZone) {
  var k = Math.floor((a11 - 2415021.076998695) / 29.530588853 + 0.5);
  var last = 0, i = 1;
  var arc = sunLongitude_(newMoonDay_(k + i, timeZone), timeZone);
  do {
    last = arc;
    i++;
    arc = sunLongitude_(newMoonDay_(k + i, timeZone), timeZone);
  } while (arc != last && i < 14);
  return i - 1;
}

/** Trả về [ngàyÂm, thángÂm, nămÂm, nhuận(0/1)] từ ngày dương lịch dd/mm/yy. */
function convertSolar2Lunar_(dd, mm, yy) {
  var timeZone = VN_TZ_OFFSET;
  var dayNumber = jdFromDate_(dd, mm, yy);
  var k = Math.floor((dayNumber - 2415021.076998695) / 29.530588853);
  var monthStart = newMoonDay_(k + 1, timeZone);
  if (monthStart > dayNumber) monthStart = newMoonDay_(k, timeZone);
  var a11 = lunarMonth11_(yy, timeZone);
  var b11 = a11, lunarYear;
  if (a11 >= monthStart) {
    lunarYear = yy;
    a11 = lunarMonth11_(yy - 1, timeZone);
  } else {
    lunarYear = yy + 1;
    b11 = lunarMonth11_(yy + 1, timeZone);
  }
  var lunarDay = dayNumber - monthStart + 1;
  var diff = Math.floor((monthStart - a11) / 29);
  var lunarLeap = 0, lunarMonth = diff + 11;
  if (b11 - a11 > 365) {
    var leapMonthDiff = leapMonthOffset_(a11, timeZone);
    if (diff >= leapMonthDiff) {
      lunarMonth = diff + 10;
      if (diff == leapMonthDiff) lunarLeap = 1;
    }
  }
  if (lunarMonth > 12) lunarMonth -= 12;
  if (lunarMonth >= 11 && diff < 4) lunarYear -= 1;
  return [lunarDay, lunarMonth, lunarYear, lunarLeap];
}

/** Trả về [ngàyDương, thángDương, nămDương] từ ngày âm lịch, hoặc [0,0,0] nếu không hợp lệ. */
function convertLunar2Solar_(lunarDay, lunarMonth, lunarYear, lunarLeap) {
  var timeZone = VN_TZ_OFFSET;
  var a11, b11;
  if (lunarMonth < 11) {
    a11 = lunarMonth11_(lunarYear - 1, timeZone);
    b11 = lunarMonth11_(lunarYear, timeZone);
  } else {
    a11 = lunarMonth11_(lunarYear, timeZone);
    b11 = lunarMonth11_(lunarYear + 1, timeZone);
  }
  var off = lunarMonth - 11;
  if (off < 0) off += 12;
  if (b11 - a11 > 365) {
    var leapOff = leapMonthOffset_(a11, timeZone);
    var leapMonth = leapOff - 2;
    if (leapMonth < 0) leapMonth += 12;
    if (lunarLeap != 0 && lunarMonth != leapMonth) {
      return [0, 0, 0];
    } else if (lunarLeap != 0 || off >= leapOff) {
      off += 1;
    }
  }
  var k = Math.floor(0.5 + (a11 - 2415021.076998695) / 29.530588853);
  var monthStart = newMoonDay_(k + off, timeZone);
  return jdToDate_(monthStart + lunarDay - 1);
}

/** Tách chuỗi "dd/mm" (ngày giỗ âm lịch, không có năm) thành {day, month}. */
function parseLunarDDMM_(s) {
  var m = String(s || '').trim().match(/^(\d{1,2})\s*[\/\-]\s*(\d{1,2})$/);
  if (!m) return null;
  var day = Number(m[1]), month = Number(m[2]);
  if (day < 1 || day > 30 || month < 1 || month > 12) return null;
  return { day: day, month: month };
}

/**
 * Danh sách ngày giỗ sắp tới trong `daysAhead` ngày kể từ hôm nay, sắp xếp gần nhất trước.
 * Với mỗi người có NgayGio hợp lệ: tính ngày dương lịch của ngày giỗ đó trong năm âm lịch
 * hiện tại; nếu đã qua thì tính cho năm âm lịch kế tiếp.
 */
function upcomingGioList_(daysAhead) {
  daysAhead = daysAhead || 60;
  var tz = Session.getScriptTimeZone() || 'Asia/Ho_Chi_Minh';
  var now = new Date();
  var todayStr = Utilities.formatDate(now, tz, 'yyyy-MM-dd');
  var today = new Date(todayStr + 'T00:00:00');
  var todaySolar = todayStr.split('-').map(Number); // [yyyy, mm, dd]
  var todayLunar = convertSolar2Lunar_(todaySolar[2], todaySolar[1], todaySolar[0]);
  var lunarYearNow = todayLunar[2];

  var sheet = getSheet_();
  var values = sheet.getDataRange().getValues();
  var headers = values[0];
  var idCol = headers.indexOf('ID');
  var nameCol = headers.indexOf('HoTen');
  var gioCol = headers.indexOf('NgayGio');
  var chucDanhCol = headers.indexOf('ChucDanh');

  var out = [];
  for (var r = 1; r < values.length; r++) {
    var lunar = parseLunarDDMM_(values[r][gioCol]);
    if (!lunar) continue;

    var candidate = solarOfLunarThisOrNextYear_(lunar.day, lunar.month, lunarYearNow, today);
    if (!candidate) continue;

    var daysLeft = Math.round((candidate.date.getTime() - today.getTime()) / 86400000);
    if (daysLeft < 0 || daysLeft > daysAhead) continue;

    out.push({
      id: values[r][idCol],
      ten: values[r][nameCol],
      chucDanh: values[r][chucDanhCol] || '',
      amLich: pad2_(lunar.day) + '/' + pad2_(lunar.month),
      duongLich: Utilities.formatDate(candidate.date, tz, 'dd/MM/yyyy'),
      conLai: daysLeft
    });
  }
  out.sort(function (a, b) { return a.conLai - b.conLai; });
  return out;
}

/** Ngày dương lịch của một ngày âm lịch (day/month, không nhuận) rơi vào năm âm `lunarYear`
 *  hoặc năm kế tiếp nếu ngày đó trong năm `lunarYear` đã qua so với `today`. */
function solarOfLunarThisOrNextYear_(day, month, lunarYear, today) {
  var r = convertLunar2Solar_(day, month, lunarYear, 0);
  var d = (r && r[0]) ? new Date(r[2] + '-' + pad2_(r[1]) + '-' + pad2_(r[0]) + 'T00:00:00') : null;
  if (!d || d.getTime() < today.getTime()) {
    var r2 = convertLunar2Solar_(day, month, lunarYear + 1, 0);
    if (r2 && r2[0]) {
      d = new Date(r2[2] + '-' + pad2_(r2[1]) + '-' + pad2_(r2[0]) + 'T00:00:00');
    } else {
      d = null;
    }
  }
  return d ? { date: d } : null;
}
