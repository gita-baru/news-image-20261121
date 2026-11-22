# Checklist pagi Minggu 22 Nov — submit v1 news-image 21 Nov

Dicek Sabtu 21 Nov 2026, 20:03 WIB. Rencana: submit v1 besok pagi (22 Nov),
deadline final Senin 23 Nov 07:00 WIB. v2 hanya di jam-jam terakhir kalau jelas lebih bagus.

## Yang SUDAH terkonfirmasi malam ini
- **F1 kualifikasi — TERKONFIRMASI.** Antonelli tercepat 1:33.893, tapi kena penalti
  5 grid (ganti power unit) → **Verstappen start dari pole**, Russell P2.
  Sumber: formula1.com, fia.com, autosport.com (21 Nov). Label "Verstappen pole"
  di v1 sudah benar, bukan lagi prediksi.

## Yang BELUM ada hasilnya malam ini — cek besok pagi
1. **ATP semifinal — BELUM MAIN.** Alcaraz–Shelton sore Turin (±20:00 WIB),
   Zverev–Medvedev malam Turin (±02:30 WIB Minggu). Final hari Minggu.
   ⚠️ JEBAKAN: beredar hasil "Sinner kalahkan Ruud 6-1, 6-2" — PALSU/SALAH.
   Sinner mundur karena cedera lutut; semifinalisnya Alcaraz, Shelton,
   Zverev, Medvedev. JANGAN pakai hasil Sinner–Ruud itu.
2. **Premier League — BELUM SELESAI.** Man City–Fulham sedang jalan
   (Fulham unggul 1-0, menit 33' saat dicek 20:03 WIB). 5 laga lain kick-off
   22:00 WIB; Newcastle–Arsenal 00:30 WIB Minggu. Semua skor final baru ada
   besok pagi.
3. **BepiColombo — BELUM TERJADI.** Burn penyisipan orbit 19:24 CET =
   **01:24 WIB Minggu**, durasi 37 menit. Konfirmasi ESA baru ada besok pagi
   (cek ESA live updates / X). Catatan: ini weak capture, awal rangkaian
   16 manuver — bukan satu burn penentu.
4. **COP31 — BELUM ADA KESEPAKATAN FINAL.** Masih deadlock; sidang penutup
   ditangguhkan Jumat 22:29 waktu setempat, draf ketiga dijanjikan Sabtu pagi.
   Cek besok pagi: kesepakatan diadopsi atau deadlock berlanjut. Yang di v1
   ("molor ke Sabtu, draf ketiga, tanpa kata phase-out fosil") masih akurat
   per malam ini.
5. **F1 balapan — BELUM MAIN, dan TIDAK BISA masuk v1 pagi.** Start Sabtu
   20:00 waktu Las Vegas = **Minggu 11:00 WIB**; pemenang baru ketahuan
   ±12:30 WIB Minggu. Jadi v1 pagi tetap pakai label TONIGHT untuk pemenang
   balapan; hasil balapan hanya bisa masuk v2 di jam-jam terakhir.

## LatAm
- Tidak ditemukan cerita LatAm yang terverifikasi bertanggal 21 Nov malam ini
  (kandidat yang ada bertanggal 19–20 Nov: toko Tesla Argentina, paket fiskal
  Senat Brasil, demo Kolombia). JANGAN tukar masuk cerita 20 Nov.
  Gempa Peru (hero v1) sudah menutup celah LatAm.

## Urutan kerja besok pagi
1. Ambil skor semifinal ATP (2 laga) + 7 skor PL + konfirmasi BepiColombo
   + status akhir COP31 → update gambar.
2. Submit v1, catat nilai dev.
3. Pemenang F1 (±12:30 WIB) + draf final COP31 kalau keluar siang → bahan v2.

## Update Sabtu 21 Nov 21:03 WIB (dicek ulang malam ini)
- **Man City–Fulham: MASIH JALAN, 1-1 menit ~75'.** Muniz 16' (Fulham),
  Anderson 57' (City). Bukan hasil final — jangan pakai skor apapun dulu.
  ⚠️ JEBAKAN BARU: beredar headline "Fulham 4-5 Man City, Haaland pecah
  rekor 100 gol" dari bbcinsight.pages.dev (BUKAN bbc.com) + artikel
  Medium dengan urutan gol yang berbeda (Haaland, Reijnders, Foden 2x…)
  — BERTENTANGAN dengan dua live feed independen (Sportradar + TNT,
  sama-sama 1-1 menit 70–75'). JANGAN pakai skor 5-4 itu.
- **ATP semifinal 1: BARU MULAI.** Alcaraz–Shelton start 20:30 WIB
  (14:30 CET), status live saat dicek 21:03 WIB — belum ada hasil.
  Zverev–Medvedev tetap 02:30 WIB Minggu.
- **COP31: MASIH BELUM ADA KESEPAKATAN.** Draf ketiga dijanjikan Sabtu
  pagi, pembicaraan lanjut Sabtu; sampai malam ini belum ada laporan
  adopsi. Status di v1 ("molor ke Sabtu, draf ketiga, tanpa kata
  phase-out fosil") masih akurat.
- 5 laga PL kick-off 22:00 WIB belum mulai saat dicek.

## Update Minggu 22 Nov 15:10 WIB — v1 FINAL DIRENDER, SIAP SUBMIT
- draw21.py diperbarui + entry.png dirender ulang (175.212 byte, sha256
  cdb25190…), commit lokal **a544a4a**. Semua 13 panel kini CONFIRMED,
  tidak ada lagi label TONIGHT. Dicek visual 1024 px + 300 px: judul hero
  dan angka besar terbaca; panel kecil tetap blur di 300 px seperti v1
  (desain 3 ukuran baca).
- COP31 dicek ulang 15:03 WIB: plenary molor ke 11:00 Antalya = 15:00 WIB,
  adopsi BELUM terkonfirmasi (khabarwire: plenary belum dibuka saat
  ditulis; europamorgenpost: belum ada kesepakatan final). Gambar menulis
  "package tabled, no fossil fuels; plenary slips to Sunday afternoon" —
  TIDAK klaim deal tercapai. Kalau plenary mengadopsi sore ini, itu bahan v2.
- ATP/F1/PL/Bepi dicek ulang independen 15:03 WIB dan cocok persis dengan
  checklist 14:03 (Wikipedia/Tennis Majors, formula1.com/FIA, AFP collated,
  Nature/ESA). Satu koreksi menit: gol Anderson City–Fulham 58' (AFP),
  bukan 57' — tidak dipakai di gambar (hanya skor).
- **Tinggal: push + submit v1** (PAT sementara via browser, standing
  approval sudah ada; submit v1 sudah disepakati user). Deadline Senin
  23 Nov 07:00 WIB (~16 jam lagi). Cek kuota dulu (3 entri, belum dipakai
  untuk kompetisi ini sejauh yang tercatat).
- v2 di jam-jam terakhir hanya kalau jelas lebih bagus: bahan v2 = hasil
  final ATP (Minggu malam) + hasil plenary COP31 kalau berubah.

## Update Minggu 22 Nov 14:03 WIB — SEMUA HASIL TERVERIFIKASI (dicek via web search)
Catatan: v1 BELUM disubmit sampai jam ini (entry.png terakhir 21 Nov 09:01).
Deadline final tetap Senin 23 Nov 07:00 WIB (~17 jam lagi). Semua item di bawah
ini sudah final dan bisa masuk v1 sebagai CONFIRMED — kecuali COP31.

1. **ATP semifinal — FINAL, TERKONFIRMASI (2 sumber independen cocok).**
   - Alcaraz kalahkan Shelton **3-6, 6-3, 7-6(1)** (comeback dari set down,
     tiebreak 7-1; Alcaraz main dengan paha dibalut pasca-MRI hamstring).
   - Zverev kalahkan Medvedev **7-6(0), 6-4** (tiebreak sempurna 7-0,
     Zverev belum kehilangan servis sepanjang minggu).
   - Final Minggu: **Alcaraz vs Zverev** (No. 1). Final itu sendiri TIDAK
     masuk v1 (baru main Minggu malam) — cukup tulis semifinal + finalis.
   Sumber: Tennis Majors, NBC Sports, Xinhua/IANS.
   Label di draw21.py yang harus diubah: "atp" dari TONIGHT ("semifinals
   tonight") → CONFIRMED dengan skor di atas.
2. **Premier League, 7 laga — SEMUA FINAL, TERKONFIRMASI (AFP collated
   + beberapa roundup cocok).**
   - Man City 1-1 Fulham (Muniz 16', Anderson 57'; gol Haaland dianulir VAR)
     → skor palsu "Fulham 4-5 Man City" TERKONFIRMASI PALSU, jangan dipakai.
   - Newcastle 2-2 Arsenal (Barnes 49', Thiaw 62'; Eze 33', Madueke 78')
   - Chelsea 1-4 Leeds (Emegha 25'; Okafor 28', 58', Calvert-Lewin 53' pen,
     Aaronson 90+1') — kemenangan pertama Leeds di Stamford Bridge sejak 1999
   - Bournemouth 2-0 Nottingham Forest (Evanilson 19', Kluivert 45+3')
   - Tottenham 2-0 Ipswich
   - Coventry 3-2 Crystal Palace (Awoniyi 5', Sakamoto 30', McNeil 85' og;
     Pino 13', Strand Larsen 45+1')
   - Aston Villa 0-0 Sunderland
   Label di draw21.py yang harus diubah: "pl" dari TONIGHT → CONFIRMED
   dengan 7 skor di atas (sorot Leeds 4-1 + City 1-1 + Newcastle 2-2).
3. **F1 Las Vegas GP — PEMENANG SUDAH KETAHUAN, TERKONFIRMASI
   (formula1.com, AP, The Race cocok).**
   - **Verstappen MENANG** (pole → menang, 1:27:39.624, kemenangan ke-75
     karier, ke-4 musim ini), Norris P2 +0.639, Piastri P3 +1.529,
     Antonelli P4, Gasly P5; 35 pergantian pimpinan, Russell tabrak tembok
     dan finis P9, Hamilton–Leclerc bertabrakan (Hamilton P7, Leclerc P10).
   - PERUBAHAN RENCANA: pemenang balapan tadinya hanya untuk v2, tapi
     sekarang sudah diketahui SEBELUM v1 disubmit — jadi v1 bisa langsung
     pakai hasil balapan sebagai CONFIRMED, bukan label TONIGHT. Ini bikin
     v1 lebih kuat dari rencana awal.
   Label di draw21.py: "f1" dari "Verstappen on pole" → "Verstappen wins
   Las Vegas GP" CONFIRMED.
4. **BepiColombo — TERKONFIRMASI BERHASIL MASUK ORBIT (AP, Nature, ESA).**
   - ESA konfirmasi 21 Nov: orbital capture tercapai setelah burn 37 menit;
     pesawat kini mengorbit Merkurius setelah 8 tahun perjalanan. Dua probe
     tetap bergabung sampai pisah 9 Des; fase sains mulai Apr 2027.
   - Ini pengunjung pertama Merkurius dalam >1 dekade, wahana ke-3 sepanjang
     sejarah (setelah Mariner 10, MESSENGER).
   Label di draw21.py: "bepi" dari TONIGHT ("fires thrusters tonight,
   aiming to orbit") → CONFIRMED "BepiColombo enters Mercury orbit".
5. **COP31 — BELUM DIADOPSI, JANGAN TULIS "DEAL TERCAPAI".**
   - Paket final 10 halaman dirilis ~02:00 waktu setempat Minggu
     (23:00 GMT Sabtu): TANPA satu pun kata "fossil fuels"/phase-out;
     target listrik 35% konsumsi energi akhir pada 2035; CCUS skala gigaton;
     tanpa angka dana adaptasi yang mengikat.
   - Batas keberatan 03:00 GMT, sidang plenary persetujuan 06:00 GMT =
     **13:00 WIB hari ini** — sedang/baru berlangsung saat checklist ini
     ditulis. Status v1 yang aman: "paket final diajukan Minggu dini hari,
     tanpa kata fossil fuels; plenary persetujuan 13:00 WIB" — cek sekali
     lagi hasil plenary SEBELUM submit; kalau sudah diadopsi, ubah jadi
     CONFIRMED "COP31 adopts deal with no fossil-fuel mention".
   - KOREKSI JAM (cek ulang 14:10 WIB): satu sumber mengutip Kurum menargetkan
     plenary 10:00–10:30 waktu setempat = 14:00–14:30 WIB, dan EU masih
     ragu menyetujui — jadi adopsi BELUM terkonfirmasi sampai jam ini.
     Jangan tulis "deal tercapai" di v1 apa pun yang terjadi; tulis
     "paket final diajukan, voting plenary Minggu siang" kecuali hasil
     adopsi sudah terkonfirmasi dari 2 sumber.

## Urutan kerja sore ini (revisi dari rencana pagi)
1. Update draw21.py: atp, pl, f1, bepi → CONFIRMED dengan hasil di atas;
   cop31 tetap sesuai status plenary 13:00 WIB (cek ulang sebelum submit).
2. Render ulang entry.png, cek keterbacaan 300 px.
3. Submit v1, catat nilai dev. Deadline Senin 23 Nov 07:00 WIB.
4. v2 di jam-jam terakhir hanya kalau jelas lebih bagus (mis. hasil final
   ATP + hasil plenary COP31 kalau berubah).
