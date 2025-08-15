# Freight & Domestic Shipping Dashboard

Aplikasi ini digunakan untuk menghitung ongkos kirim internasional dan domestik dengan cepat, berbasis data negara asal dan kategori barang.

---

## Fitur

### 1. Login & Autentikasi
- Pengguna harus login untuk mengakses dashboard.
- Tersedia tombol logout di header.

### 2. Dashboard & CRUD
- **Countries:** Tambah, edit, hapus data negara asal internasional.
- **Categories:** Tambah, edit, hapus kategori barang.

### 3. Freight Calculator
- Menghitung ongkos kirim berdasarkan:
  - Negara asal (Internasional)
  - Kategori barang
  - Asal & tujuan domestik (Provinsi / Kota / Kecamatan)
  - Berat barang

- Menampilkan hasil:
  - Origin (Internasional)
  - Destination (Domestik)
  - Category
  - International Price
  - Domestic Price
  - Total Price

---
## Untuk Input Form Domestic nya 
- Harus menggunakan key dari raja ongkir
  
## Cara Menjalankan

1. Clone repository:  
```bash
git clone https://github.com/username/Blueraycargo_project.git
cd freight-dashboard
cd env
cd Scripts
activate
python manage.py make migrations
python manage.py migrate
python manage.py runserver
