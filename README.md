# Tebak Profesi

Permainan tebak-tebakan edukatif berbasis web untuk anak usia 5-6 tahun. Anak-anak menebak nama profesi berdasarkan gambar, sementara orang tua dapat mengunggah gambar profesi baru dan jawaban melalui antarmuka admin.

---

## Tentang Proyek

**Target Pengguna:** Anak-anak usia 5-6 tahun
**Bahasa:** Indonesia (Bahasa Indonesia)
**Framework:** Flask (Python) dengan database SQLite3
**Arsitektur:** Pattern MVC sederhana dengan Jinja2 templating

### Fitur

- **Antarmuka Admin (Mama Papa):** Upload gambar profesi dengan jawaban yang benar
- **Antarmuka Permainan (Vanya):** Permainan tebak-tebakan yang ramah anak dengan:
  - Pilihan jumlah soal (5, 10, 15, atau 20 soal)
  - Pelacakan skor real-time dengan bintang
  - Umpan balik instan dengan perayaan confetti
  - Desain cerah dan warna-warni yang dioptimalkan untuk anak-anak
- **Responsif Mobile:** Berfungsi di tablet dan smartphone

---

## Cara Menjalankan

### Prasyarat

- Python 3.8+
- Virtual environment (venv)

### Instalasi

1. **Navigasi ke direktori proyek:**
   ```bash
   cd /home/etc/claude-code/vanya-game
   ```

2. **Aktifkan virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   Atau jika Anda menggunakan Windows:
   ```bash
   venv\Scripts\activate
   ```

3. **Instal dependensi** (jika belum terinstal):
   ```bash
   pip install -r requirements.txt
   ```

### Menjalankan Aplikasi

1. **Pastikan virtual environment aktif:**
   ```bash
   source venv/bin/activate
   ```

2. **Jalankan server Flask:**
   ```bash
   python3 app.py
   ```

3. **Buka browser dan navigasikan ke:**
   ```
   http://localhost:5000
   ```

4. **Untuk menghentikan server:** Tekan `Ctrl+C` di terminal

---

## Struktur Proyek

```
vanya-game/
├── app.py                      # Aplikasi Flask utama
├── database.py                 # Fungsi database SQLite
├── requirements.txt            # Dependensi Python
├── venv/                       # Virtual environment (JANGAN COMMIT)
├── tebak_profesi.db           # Database SQLite (dibuat otomatis)
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheet utama
│   ├── js/
│   │   └── game.js            # Logika permainan
│   └── images/
│       └── uploads/           # Gambar profesi yang diunggah pengguna
├── templates/
│   ├── base.html              # Template dasar
│   ├── index.html             # Halaman landing
│   ├── admin.html             # Halaman upload admin
│   ├── select_count.html      # Pemilihan jumlah soal
│   ├── game.html              # Halaman permainan utama
│   └── result.html            # Halaman hasil
└── docs/
    └── plans/                 # Dokumen desain dan implementasi
```

---

## Cara Menguji

### Checklist Pengujian Manual

#### 1. Halaman Landing
- [ ] Halaman dimuat di `http://localhost:5000`
- [ ] Kartu "Mama Papa" dan "Vanya" keduanya terlihat
- [ ] Desain terlihat cerah dan warna-warni
- [ ] Efek hover berfungsi pada tombol

#### 2. Alur Admin (Mama Papa)
- [ ] Navigasi ke `/admin` atau klik "Mama Papa"
- [ ] Form upload ditampilkan dengan benar
- [ ] Dapat memilih file gambar (png, jpg, jpeg, webp)
- [ ] Dapat mengetik nama profesi
- [ ] Tombol upload berfungsi
- [ ] Gambar yang diunggah muncul dalam daftar
- [ ] Tombol hapus menghapus gambar
- [ ] Pesan flash muncul (sukses/error)

#### 3. Alur Permainan (Vanya - Tanpa Data)
- [ ] Navigasi ke `/play` atau klik "Vanya"
- [ ] Menampilkan pesan "tidak ada data" saat database kosong
- [ ] Menyarankan orang tua untuk upload terlebih dahulu

#### 4. Alur Permainan (Vanya - Dengan Data)
- [ ] Tombol jumlah (5, 10, 15, 20) muncul berdasarkan data yang tersedia
- [ ] Mengklik tombol jumlah memulai permainan
- [ ] Gambar profesi pertama ditampilkan
- [ ] Kolom input jawaban menerima teks
- [ ] Tombol submit berfungsi
- [ ] Jawaban benar memicu confetti + pesan "Benar!"
- [ ] Jawaban salah menampilkan jawaban yang benar
- [ ] Skor diperbarui dengan benar
- [ ] Semua soal ditanyakan sebelum menampilkan hasil

#### 5. Halaman Hasil
- [ ] Menampilkan skor yang benar (misalnya "4 dari 5")
- [ ] Pesan ucapan selamat muncul
- [ ] Perayaan confetti diputar
- [ ] Tombol "Main Lagi!" memulai permainan baru
- [ ] Tombol "Ke Home" kembali ke halaman landing

#### 6. Responsivitas Mobile
- Buka DevTools browser (F12) dan aktifkan toolbar perangkat
- [ ] Layout menyesuaikan dengan layar mobile
- [ ] Tombol ramah sentuhan (ukuran cukup besar)
- [ ] Teks tetap dapat dibaca
- [ ] Gambar diskala dengan benar

### Menambahkan Data Tes

Upload 5-10 gambar profesi contoh melalui halaman admin:
- Dokter (Doctor)
- Guru (Teacher)
- Polisi (Police)
- Petani (Farmer)
- Nelayan (Fisherman)
- Pilot
- Masinis (Train Driver)
- Koki (Chef)

---

## Catatan Pengembangan

- **Secret Key:** Saat ini diatur ke nilai placeholder - ubah untuk produksi
- **Debug Mode:** Diaktifkan (`debug=True`) - nonaktifkan untuk produksi
- **Batas Upload:** Maksimal 5MB per file
- **Format yang Diizinkan:** PNG, JPG, JPEG, WebP
- **Database:** SQLite3 dengan tabel `professions` tunggal

---

## Kompatibilitas Browser

Diuji pada browser modern:
- Chrome/Chromium (direkomendasikan)
- Firefox
- Safari
- Edge

Versi minimum: Browser apa pun dari tahun 2018 ke atas (untuk dukungan CSS flexbox dan gradient)

---

## Lisensi

Proyek ini dibuat untuk tujuan edukasi.

---

## Dukungan

Untuk pertanyaan atau masalah, silakan hubungi pengembang proyek.
