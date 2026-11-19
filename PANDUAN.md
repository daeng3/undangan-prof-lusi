# Panduan Undangan Pengukuhan Guru Besar

Undangan digital untuk **Pengukuhan Guru Besar Prof. Dr. apt. Lusi Nurdianti, M.Si.**
Senin, 30 November 2026 · 08.00 WIB · BTH Convention Hall, Tasikmalaya.

---

## 1. Isi paket

| Berkas | Fungsi |
| --- | --- |
| `index.html` | Undangan lengkap (foto sudah menyatu di dalam file, bisa dibuka tanpa internet) |
| `share.jpg` | Gambar pratinjau saat tautan dikirim di WhatsApp (1200 × 630) |
| `Code.gs` | Backend rekap konfirmasi di Google Sheets |
| `PANDUAN.md` | Berkas ini |

`Undangan Pengukuhan.html` adalah draf lama dan tidak dipakai lagi.

---

## 2. Memasang rekap konfirmasi (sekali saja, ±10 menit)

Tanpa langkah ini undangan tetap bisa dibuka dan dibagikan, tetapi konfirmasi tamu hanya
tersimpan di perangkat tamu masing-masing (mode pratinjau) dan **tidak** terkumpul ke panitia.

1. Buka <https://sheets.new> → beri nama, misalnya **Rekap Konfirmasi Pengukuhan**.
2. Menu **Extensions / Ekstensi → Apps Script**.
3. Hapus seluruh isi `Code.gs` di editor, lalu tempel seluruh isi `Code.gs` dari paket ini → **Save**.
4. Di daftar fungsi, pilih `siapkan` → **Run**. Saat diminta, pilih akun Google lalu
   **Allow / Izinkan**. Setelah selesai, spreadsheet akan memiliki dua sheet:
   `RSVP` (data mentah) dan `Rekap` (ringkasan jumlah hadir, tidak hadir, dan kursi).
5. **Deploy → New deployment → pilih "Web app"**
   - Description: `undangan`
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Klik **Deploy** → **Authorize access** → izinkan.
6. Salin **Web app URL** yang berakhiran `/exec`
   (contoh: `https://script.google.com/macros/s/AKfycb.../exec`).
7. Buka `index.html` dengan editor teks, cari `apiUrl` (Ctrl+F), lalu tempel URL tadi:

   ```js
   apiUrl: "https://script.google.com/macros/s/AKfycb.../exec",
   ```

8. Simpan berkas. Karena folder ini sudah berupa repositori Git, jalankan:

   ```powershell
   git add index.html
   git commit -m "atur apiUrl rekap"
   git push
   ```

   Vercel akan deploy otomatis bila proyeknya diimpor dari GitHub; jika deploy manual, jalankan
   `npx vercel --prod`.

> **Uji cepat koneksi:** buka `URL_ANDA/exec?action=rekap` di browser.
> - `{"ok":true,"data":[]}` (atau berisi daftar nama) → backend siap.
> - Muncul halaman login Google / HTML → akses belum **Anyone**.
> - `{"ok":false,"pesan":"..."}` → jalankan fungsi `siapkan`, lalu cek **Executions** di Apps Script.

> **Kalau `Code.gs` diubah:** Deploy → **Manage deployments** → ikon pensil → Version: **New version**
> → Deploy. URL tetap sama; tanpa langkah ini perubahan tidak ikut aktif.

> **Catatan penting:** akses harus **Anyone**, bukan "Anyone with Google account".
> Jika memakai akun Google Workspace kampus, kebijakan organisasi mungkin membatasi opsi ini —
> dalam hal itu gunakan akun Gmail pribadi panitia.

---

## 3. Nomor WhatsApp panitia (opsional)

Bila `apiUrl` belum dipasang, undangan dapat mengirim konfirmasi lewat WhatsApp:

```js
waPanitia: "6281234567890",   // format 62..., tanpa tanda + dan tanpa spasi
```

- Jika `apiUrl` **diisi**, konfirmasi masuk ke Google Sheets dan rekap tampil di halaman.
- Jika `apiUrl` **kosong** dan `waPanitia` diisi, tombol konfirmasi membuka WhatsApp berisi pesan siap kirim.
- Jika keduanya kosong, pesan konfirmasi disalin otomatis agar tamu mengirimnya sendiri.

---

## 4. Mengunggah ke internet (gratis)

### Cara termudah — Netlify Drop

1. Buat folder baru, isi dengan **`index.html`** dan **`share.jpg`**.
2. Buka <https://app.netlify.com/drop>.
3. Tarik folder tersebut ke halaman itu, tunggu sampai selesai.
4. Anda mendapat tautan seperti `https://nama-acak.netlify.app` — bisa diganti namanya di
   **Site configuration → Change site name** (misalnya `pengukuhan-lusi-nurdianti`).

### Alternatif 1 — Vercel (lewat terminal, ±5 menit)

Vercel **tidak menerima unggah folder lewat dashboard**; deploy dilakukan melalui Git atau CLI.
Cara tercepat untuk paket ini adalah CLI, karena tidak perlu membuat repositori.

1. Pastikan Node.js terpasang: buka PowerShell, jalankan `node -v` (harus muncul nomor versi).
2. Masuk ke folder ini, lalu jalankan:

   ```powershell
   npx vercel login
   npx vercel --prod
   ```

   Login sekali lewat browser yang terbuka otomatis.
3. Jawab pertanyaan CLI (urutan/wording dapat sedikit berbeda):
   - *Set up and deploy?* → **Y**
   - *Which scope?* → pilih akun sendiri
   - *Link to existing project?* → **N**
   - *What's your project's name?* → mis. `undangan-pengukuhan` (huruf kecil, tanda hubung)
   - *In which directory is your code located?* → `./`
   - *Want to modify these settings?* → **N**
4. Selesai. Tautan produksi muncul, mis. `https://undangan-pengukuhan.vercel.app`.

Folder ini sudah berisi `.vercelignore`, sehingga yang diunggah hanya `index.html` dan `share.jpg`
(foto mentah, skrip, dan dokumen kerja tidak ikut).

**Memperbarui undangan:** sunting `index.html` → jalankan `npx vercel --prod` lagi.
Bila ingin otomatis, hubungkan folder ini ke repositori GitHub lalu impor di dashboard Vercel.

**Catatan khusus Vercel:**
- Jangan mengaktifkan **Deployment Protection** untuk Production — tamu akan diminta login.
- Pastikan `index.html` tetap di root (sudah begitu). Tidak perlu build command; framework = *Other*.
- Paket gratis **Hobby** ditujukan untuk proyek non-komersial dan kuotanya jauh di atas kebutuhan
  undangan; rincian di <https://vercel.com/pricing>. Untuk kegiatan resmi kampus, gunakan akun
  yang memang disediakan institusi bila ada.
- Domain kampus dapat ditambahkan di **Settings → Domains**.

### Alternatif 2 — GitHub Pages atau Cloudflare Pages
- **GitHub Pages**: unggah `index.html` + `share.jpg` ke repositori, aktifkan Pages di
  **Settings → Pages** (branch `main`, folder `/root`).
- **Cloudflare Pages**: mendukung unggah folder langsung lewat dashboard, mirip Netlify Drop.
- Hosting resmi kampus, bila tersedia.

> Undangan harus dibuka lewat tautan **https://**. Membuka `index.html` langsung dari komputer
> (file://) tidak dapat terhubung ke backend, dan pratinjau WhatsApp tidak akan muncul.

---

## 5. Uji sebelum disebar

Lakukan di ponsel, bukan hanya di komputer:

- [ ] Sampul terbuka, tombol **Buka Undangan** berfungsi.
- [ ] Foto, nama, tanggal, dan alamat tampil benar.
- [ ] Hitung mundur berjalan.
- [ ] Susunan acara lengkap 11 poin.
- [ ] Isi konfirmasi → muncul pesan berhasil → nama tampil di **Rekap Konfirmasi**.
- [ ] Cek baris baru di sheet `RSVP` (waktu, nama, instansi, kehadiran, jumlah, pesan).
- [ ] Tombol **Buka Google Maps** membuka lokasi yang benar.
- [ ] Tombol **Simpan ke Kalender** menghasilkan entri 30 November 2026, 08.00 WIB.
- [ ] Tombol **Bagikan** membuka WhatsApp.
- [ ] Kirim tautan ke diri sendiri di WhatsApp untuk melihat pratinjau gambar.

Setelah uji, hapus baris percobaan di sheet `RSVP` agar tidak muncul di rekap.

---

## 6. Membagikan lewat WhatsApp

### Tautan umum
```
https://situs-anda.netlify.app/
```

### Tautan personal (nama tamu muncul di sampul)
```
https://situs-anda.netlify.app/?to=Asep%20Hidayat
https://situs-anda.netlify.app/?to=Prof.%20Dr.%20H.%20Asep%20Hidayat%2C%20M.Si.
```
Spasi ditulis `%20`, koma ditulis `%2C`. Nama otomatis terisi pada formulir konfirmasi,
sehingga tamu tinggal memilih status kehadiran.

**Membuat banyak tautan sekaligus di Google Sheets:**

| A | B |
| --- | --- |
| Nama Tamu | Tautan |
| Asep Hidayat | `="https://situs-anda.netlify.app/?to="&ENCODEURL(A2)` |

Tarik formula ke bawah, lalu salin kolom B satu per satu ke WhatsApp.

### Contoh teks pesan

```
Assalamu'alaikum wr. wb.

Dengan hormat,
Bersama ini kami sampaikan undangan Pengukuhan Guru Besar
Prof. Dr. apt. Lusi Nurdianti, M.Si.

Senin, 30 November 2026 · 08.00 WIB
BTH Convention Hall, Tasikmalaya

Undangan lengkap dan konfirmasi kehadiran:
https://situs-anda.netlify.app/?to=Nama%20Tamu

Merupakan suatu kehormatan bagi kami apabila Bapak/Ibu
berkenan hadir dan memberikan doa restu.

Panitia Pengukuhan Guru Besar
Universitas Bakti Tunas Husada
```

> Kirim satu per satu (bukan broadcast massal tanpa izin) agar pesan tidak ditandai spam
> dan tautan personal tetap tepat sasaran.

---

## 7. Mengubah isi undangan

Semua pengaturan utama berada di satu tempat: blok `CONFIG` di bagian bawah `index.html`.

```js
const CONFIG = {
  apiUrl: "",                        // URL Apps Script .../exec
  waPanitia: "",                     // contoh "6281234567890"
  nama: "Prof. Dr. apt. Lusi Nurdianti, M.Si.",
  mulai: "2026-11-30T01:00:00Z",     // 08.00 WIB (UTC+7)
  selesai: "2026-11-30T04:00:00Z",   // 11.00 WIB
  tempat: "BTH Convention Hall",
  alamat: "Jl. Letjen Mashudi No. 20, ..."
};
```

Selain `CONFIG`, teks yang tampil di halaman juga ditulis langsung di badan HTML
( bagian detail acara, daftar susunan acara, sambutan, dan footer) sehingga bisa diubah
tanpa mengganggu skrip.

**Mengganti foto:** ganti nilai `src` pada baris `<img src="data:image/jpeg;base64,...">`
menjadi `potret.jpg`, lalu unggah `potret.jpg` bersama `index.html`.
Cara ini lebih ringan daripada menyisipkan base64 baru.

**Mengubah susunan acara:** sunting daftar `<ol class="rundown">`; setiap butir berbentuk
`<li><span class="no">01</span><span class="txt">Pembukaan</span></li>`.

---

## 8. Catatan teknis dan batasan

- **Data tamu** tersimpan di Google Sheets milik panitia; undangan tidak menyimpan data di tempat lain.
- **Daftar konfirmasi dan ucapan tampil publik** di halaman (nama, instansi, status, dan pesan).
  Ini disengaja agar tamu melihat rekap seperti yang diminta. Jika tidak diinginkan, hapus blok
  `<div class="rekap" id="rekapBox">` dan/atau section `<section ... id="ucapan">` dari `index.html`
  — data tetap masuk ke sheet.
- **Nama yang sama akan memperbarui baris lama**, bukan menambah baris baru, sehingga tamu bisa
  mengubah konfirmasinya.
- **Rekap menampilkan maksimal 300 konfirmasi terbaru.** Data penuh tetap ada di sheet.
- **Kuota Apps Script** gratis jauh lebih besar daripada kebutuhan ratusan tamu; batas resmi dapat
  dilihat di Apps Script → **Project Settings → Quotas**. Untuk acara besar, pantau di hari-H.
- **Tanpa backend**, undangan tetap berfungsi penuh kecuali rekap bersama; konfirmasi tersimpan
  di perangkat tamu (mode pratinjau) dan tidak terkirim ke panitia.
- **Tautan `?buka=1`** melewati sampul — berguna untuk pratinjau cepat atau layar informasi di lokasi.
- **Cetak/PDF:** menu cetak browser akan menghasilkan versi rapi tanpa sampul dan tombol.

---

## 9. Pemecahan masalah

| Gejala | Penyebab dan solusi |
| --- | --- |
| "Rekap belum dapat dimuat" | `apiUrl` salah, deployment belum "Anyone", atau halaman dibuka lewat `file://`. Perbaiki, lalu **Deploy → Manage deployments → Edit → New version**. |
| Konfirmasi tidak masuk ke sheet | Buka Apps Script → **Executions** untuk melihat pesan galat. Pastikan fungsi `siapkan` sudah dijalankan. |
| Pratinjau WhatsApp tanpa gambar | `og:image` masih relatif. Ganti menjadi `https://situs-anda/share.jpg`, unggah ulang, lalu uji tautan dengan `?v=2`. |
| Pratinjau lama masih muncul | WhatsApp menyimpan cache. Tunggu beberapa jam atau bagikan dengan parameter tambahan. |
| Nama tamu tidak muncul di sampul | Parameter harus `?to=`, bukan `?nama=`. Pastikan spasi ditulis `%20`. |
| Font terlihat berbeda | Undangan memakai Google Fonts (Cormorant Garamond & Jost). Tanpa internet, tampilan memakai Georgia — tetap rapi. |
| Rekap kosong padahal sheet berisi | Pastikan data ada di sheet bernama tepat `RSVP` dan kolom B berisi nama. |
