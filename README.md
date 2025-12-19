# 🎱 Permainan Billiard (Python & Pygame)

Permainan **Billiard** ini dikembangkan menggunakan bahasa pemrograman **Python** dengan pustaka utama **Pygame**.  
Aplikasi ini bersifat **cross-platform**, sehingga dapat dijalankan pada **Windows, macOS, dan Linux** selama Python telah terpasang dengan benar.

---

## Teknologi yang Digunakan
- Python (disarankan versi 3.8 ke atas)
- Pygame

---

## Panduan Instalasi, Menjalankan, dan Penggunaan Aplikasi

Ikuti langkah-langkah berikut secara berurutan:

1. Kloning repositori dari GitHub  
   git clone https://github.com/AdriLorenzo99/biliard.git

2. Masuk ke direktori proyek  
   cd biliard

3. Instal pustaka yang dibutuhkan  
   pip install pygame

4. Jalankan aplikasi  
   python biliard_final.py

Setelah dijalankan, aplikasi akan membuka jendela permainan berukuran **960 x 540 piksel**.  
Jendela bersifat **resizable** dan akan menyesuaikan skala tampilan tanpa merusak rasio permainan.

---

## Panduan Penggunaan dan Kontrol

### Menu Utama
- Gunakan tombol **Panah Atas / Panah Bawah** pada keyboard untuk memilih mode permainan:
  - 1 Player
  - 2 Player
  - Exit
- Tekan **Enter** untuk mengonfirmasi pilihan mode permainan.

---

### Kontrol Dalam Permainan
- **Membidik**  
  Gerakkan **Mouse** untuk mengatur sudut bidikan stik biliar.  
  Garis bantu (*Guideline*) akan membantu memproyeksikan arah pukulan.

- **Kekuatan Pukulan**  
  Klik dan tahan **Tombol Kiri Mouse**, tarik stik ke belakang untuk mengatur kekuatan pukulan, lalu lepaskan untuk memukul bola putih.

- **Ball-in-Hand**  
  Jika terjadi pelanggaran (*foul / scratch*), klik kiri pada area meja yang valid untuk menempatkan kembali bola putih.

---

### Kontrol Sistem
- **Fullscreen** : Tekan tombol **F**
- **Pause / Menu** : Tekan tombol **ESC**  
  Akan muncul menu jeda (*Pause Menu*) yang berisi opsi:
  - Restart
  - Kembali ke Main Menu

---
## Catatan
Pastikan seluruh dependensi telah terinstal dengan benar agar permainan dapat berjalan tanpa kendala.
