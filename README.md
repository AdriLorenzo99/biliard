Untuk dapat menjalankan aplikasi di lingkungan lokal, pengguna perlu mengikuti langkah-langkah instalasi berikut ini:
Prasyarat Sistem: Pastikan perangkat Anda telah terpasang Python versi 3.x. Anda dapat memverifikasi instalasi dengan menjalankan perintah python --version di terminal atau CMD.
Kloning Repositori: Buka terminal atau git bash, lalu arahkan ke folder direktori tujuan Anda. Jalankan perintah berikut untuk mengunduh seluruh kode sumber dari repositori GitHub: git clone https://github.com/AdriLorenzo99/biliard.git
Instalasi Dependensi: Masuk ke dalam direktori proyek yang baru dikloning dengan perintah cd biliard. Setelah itu, pasang library Pygame sebagai mesin penggerak utama permainan dengan perintah: pip install pygame
Menjalankan Program: Setelah seluruh persiapan selesai, jalankan file utama program dengan perintah: python biliard_final.py

Berikut adalah panduan kontrol yang tersedia:

Navigasi Menu Utama:
Gunakan tombol PANAH ATAS/BAWAH pada keyboard untuk memilih mode permainan (1 Player, 2 Player, atau Exit Game).
Tekan ENTER untuk mengonfirmasi pilihan Anda.
Kontrol Inti Permainan:
Membidik (Aiming): Gerakkan kursor Mouse di sekitar bola putih untuk menentukan arah pukulan. Garis bantu bidik (Guideline) akan secara otomatis memproyeksikan arah bola.
Mengatur Kekuatan (Power): Klik dan tahan Klik Kiri Mouse, lalu tarik menjauh dari bola putih. Semakin jauh tarikan, semakin besar tenaga pukulan yang dihasilkan, yang ditunjukkan oleh indikator pada stik.
Memukul (Shooting): Lepaskan Klik Kiri Mouse untuk mengeksekusi tembakan.
Fungsi Tambahan:
Pause/Unpause: Tekan tombol ESC untuk membuka menu jeda atau melanjutkan permainan.
Layar Penuh (Fullscreen): Tekan tombol 'F' pada keyboard untuk berganti antara mode jendela dan mode layar penuh.
Ball-in-Hand: Jika terjadi pelanggaran, pemain lawan cukup melakukan Klik Kiri pada area meja yang diinginkan untuk menempatkan bola putih kembali.
