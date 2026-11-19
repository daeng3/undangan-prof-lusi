/**
 * Backend rekap konfirmasi — Undangan Pengukuhan Guru Besar
 * Prof. Dr. apt. Lusi Nurdianti, M.Si. — Universitas Bakti Tunas Husada
 *
 * Cara pakai singkat (detail di PANDUAN.md):
 *   1. Buat Google Sheets baru → menu Extensions/Ekstensi → Apps Script.
 *   2. Hapus isi Code.gs, tempel seluruh berkas ini, lalu Save.
 *   3. Jalankan fungsi `siapkan` sekali (izinkan akses saat diminta).
 *   4. Deploy → New deployment → Web app
 *        Execute as : Me
 *        Who has access : Anyone
 *      Salin URL yang berakhiran /exec.
 *   5. Tempel URL tersebut ke CONFIG.apiUrl di index.html.
 */

var SHEET_NAME = 'RSVP';
var REKAP_NAME = 'Rekap';
var HEADERS = ['Waktu', 'Nama', 'Instansi', 'Kehadiran', 'Jumlah Orang', 'Pesan'];

/** Menyiapkan sheet RSVP + sheet ringkasan. Aman dijalankan berulang. */
function siapkan() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.setSpreadsheetTimeZone('Asia/Jakarta');

  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) sh = ss.insertSheet(SHEET_NAME);
  if (sh.getLastRow() === 0) {
    sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  }
  sh.getRange(1, 1, 1, HEADERS.length)
    .setFontWeight('bold')
    .setFontColor('#e8d3a2')
    .setBackground('#0b2133')
    .setVerticalAlignment('middle');
  sh.setFrozenRows(1);
  sh.setRowHeight(1, 32);
  sh.setColumnWidth(1, 150);
  sh.setColumnWidth(2, 220);
  sh.setColumnWidth(3, 240);
  sh.setColumnWidth(4, 110);
  sh.setColumnWidth(5, 110);
  sh.setColumnWidth(6, 320);
  sh.getRange('A2:A').setNumberFormat('dd/MM/yyyy HH:mm');
  if (!sh.getFilter()) sh.getRange(1, 1, Math.max(sh.getLastRow(), 2), HEADERS.length).createFilter();

  var rk = ss.getSheetByName(REKAP_NAME);
  if (!rk) rk = ss.insertSheet(REKAP_NAME);
  rk.clear();
  rk.getRange('A1').setValue('RINGKASAN KONFIRMASI').setFontWeight('bold').setFontSize(12);
  rk.getRange('A3').setValue('Total konfirmasi');
  rk.getRange('B3').setFormula('=COUNTA(' + SHEET_NAME + '!B2:B)');
  rk.getRange('A4').setValue('Hadir');
  rk.getRange('B4').setFormula('=COUNTIF(' + SHEET_NAME + '!D2:D,"Hadir")');
  rk.getRange('A5').setValue('Tidak hadir');
  rk.getRange('B5').setFormula('=COUNTIF(' + SHEET_NAME + '!D2:D,"Tidak hadir")');
  rk.getRange('A6').setValue('Perkiraan jumlah kursi');
  rk.getRange('B6').setFormula('=SUMIF(' + SHEET_NAME + '!D2:D,"Hadir",' + SHEET_NAME + '!E2:E)');
  rk.getRange('A8').setValue('Diperbarui');
  rk.getRange('B8').setFormula('=NOW()').setNumberFormat('dd/MM/yyyy HH:mm');
  rk.getRange('A3:A6').setFontWeight('bold');
  rk.setColumnWidth(1, 210);
  rk.setColumnWidth(2, 120);

  return 'Siap. Sheet "' + SHEET_NAME + '" dan "' + REKAP_NAME + '" sudah disiapkan.';
}

/** Titik masuk permintaan GET (dipakai undangan melalui JSONP). */
function doGet(e) {
  var p = (e && e.parameter) || {};
  var cb = String(p.callback || '').replace(/[^A-Za-z0-9_$.]/g, '').slice(0, 64);
  var hasil;
  try {
    var aksi = String(p.action || 'rekap');
    if (aksi === 'kirim') {
      hasil = { ok: true, data: simpanKonfirmasi_(p) };
    } else {
      hasil = { ok: true, data: ambilRekap_() };
    }
  } catch (err) {
    hasil = { ok: false, pesan: String((err && err.message) || err) };
  }
  var body = cb ? cb + '(' + JSON.stringify(hasil) + ');' : JSON.stringify(hasil);
  return ContentService.createTextOutput(body)
    .setMimeType(cb ? ContentService.MimeType.JAVASCRIPT : ContentService.MimeType.JSON);
}

/** Titik masuk POST (cadangan; mengembalikan JSON biasa). */
function doPost(e) {
  var p = {};
  try {
    p = JSON.parse((e && e.postData && e.postData.contents) || '{}');
  } catch (err) {
    p = (e && e.parameter) || {};
  }
  var hasil;
  try {
    if (String(p.action || 'kirim') === 'kirim') {
      hasil = { ok: true, data: simpanKonfirmasi_(p) };
    } else {
      hasil = { ok: true, data: ambilRekap_() };
    }
  } catch (err2) {
    hasil = { ok: false, pesan: String((err2 && err2.message) || err2) };
  }
  return ContentService.createTextOutput(JSON.stringify(hasil))
    .setMimeType(ContentService.MimeType.JSON);
}

/** Menyimpan satu konfirmasi. Nama yang sama akan memperbarui baris lama. */
function simpanKonfirmasi_(p) {
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sh) throw new Error('Sheet "' + SHEET_NAME + '" belum ada. Jalankan fungsi siapkan.');

    var nama = bersihkan_(p.nama, 120);
    if (nama.length < 2) throw new Error('Nama wajib diisi.');

    var status = String(p.kehadiran || '').toLowerCase();
    var kehadiran = status.indexOf('tidak') >= 0 ? 'Tidak hadir'
      : (status.indexOf('hadir') >= 0 ? 'Hadir' : '');
    if (!kehadiran) throw new Error('Status kehadiran tidak valid.');

    var jumlah = parseInt(p.jumlah, 10);
    if (isNaN(jumlah) || jumlah < 1) jumlah = 1;
    if (jumlah > 10) jumlah = 10;

    var baris = [
      new Date(),
      nama,
      bersihkan_(p.instansi, 160),
      kehadiran,
      kehadiran === 'Hadir' ? jumlah : 0,
      bersihkan_(p.pesan, 500)
    ];

    var data = sh.getDataRange().getValues();
    var target = -1;
    for (var i = 1; i < data.length; i++) {
      if (String(data[i][1]).trim().toLowerCase() === nama.toLowerCase()) {
        target = i + 1; // nomor baris di sheet (1-based, +1 untuk header)
        break;
      }
    }

    if (target > 0) {
      sh.getRange(target, 1, 1, baris.length).setValues([baris]);
    } else {
      sh.appendRow(baris);
    }
    SpreadsheetApp.flush();

    return { nama: nama, kehadiran: kehadiran, jumlah: baris[4] };
  } finally {
    lock.releaseLock();
  }
}

/** Mengambil daftar konfirmasi terbaru (maksimal 300) untuk ditampilkan. */
function ambilRekap_() {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  if (!sh) throw new Error('Sheet "' + SHEET_NAME + '" belum ada. Jalankan fungsi siapkan.');

  var last = sh.getLastRow();
  if (last < 2) return [];

  var values = sh.getRange(2, 1, last - 1, HEADERS.length).getValues();
  var out = [];
  for (var i = 0; i < values.length; i++) {
    var r = values[i];
    var nama = String(r[1] || '').trim();
    if (!nama) continue;
    var waktu = r[0] instanceof Date ? r[0].toISOString() : String(r[0] || '');
    out.push({
      nama: nama,
      instansi: String(r[2] || '').trim(),
      kehadiran: String(r[3] || '').trim(),
      jumlah: Number(r[4]) || 0,
      pesan: String(r[5] || '').trim(),
      waktu: waktu
    });
  }
  out.sort(function (a, b) { return String(b.waktu).localeCompare(String(a.waktu)); });
  return out.slice(0, 300);
}

/** Membersihkan teks masukan: buang karakter kontrol dan batasi panjang. */
function bersihkan_(nilai, maks) {
  return String(nilai == null ? '' : nilai)
    .replace(/[\u0000-\u001f\u007f]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, maks || 200);
}
