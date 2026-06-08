# Clustering Trafik Jaringan IoT Menggunakan K-Means pada Dataset RT-IoT2022

## Identitas Kelompok

**Kelompok 3**

| No. | Nama Siswa | NIM |
|---|---|---|
| 1 | Nadhif Dafa Aditra | 25032014029 |
| 2 | Narendra Farel Arivanto | 25032014021 |
| 3 | Fahmi Bima Yudhistira | 25032014011 |

> Catatan: bagian nama dan NIM dapat diganti sesuai identitas anggota kelompok.

## Deskripsi Program

Program ini merupakan implementasi algoritma **K-Means Clustering** untuk mengelompokkan data trafik jaringan Internet of Things (IoT) berdasarkan karakteristik aliran data jaringan. Dataset yang digunakan adalah **RT-IoT2022** dengan file bernama `RT_IOT2022.csv`.

Terdapat dua file program utama, yaitu:

1. `kmeans_iot_k_diawal.py`  
   Program ini menjalankan K-Means dengan jumlah cluster atau nilai **K ditentukan sejak awal**, yaitu `k = 3`. Proses iterasi berhenti ketika label cluster tidak mengalami perubahan lagi atau ketika mencapai batas maksimum iterasi.

2. `kmeans_iot_threshold.py`  
   Program ini menjalankan K-Means dengan nilai **threshold** sebagai batas perubahan centroid. Iterasi akan berhenti apabila perubahan posisi centroid sudah lebih kecil atau sama dengan nilai threshold, yaitu `0.001`.

Kedua program membandingkan tiga metode perhitungan jarak, yaitu **Euclidean Distance**, **Manhattan Distance**, dan **Minkowski Distance**. Hasil clustering kemudian divisualisasikan dalam bentuk grafik sebaran data berdasarkan `flow_duration` dan `flow_pkts_per_sec`.

## Latar Belakang

Perkembangan perangkat Internet of Things (IoT) menyebabkan peningkatan jumlah lalu lintas data pada jaringan. Setiap perangkat IoT dapat menghasilkan pola komunikasi yang berbeda, baik berupa trafik normal maupun trafik yang berpotensi sebagai serangan. Oleh karena itu, diperlukan metode analisis data yang mampu mengelompokkan pola trafik berdasarkan kemiripan karakteristiknya.

Salah satu metode yang dapat digunakan adalah **K-Means Clustering**. Metode ini termasuk ke dalam algoritma unsupervised learning yang dapat mengelompokkan data tanpa harus menggunakan label sebagai acuan utama. Dalam program ini, label asli `Attack_type` tetap digunakan sebagai informasi tambahan untuk melihat komposisi jenis serangan atau trafik pada setiap cluster yang terbentuk.

Melalui pendekatan ini, data trafik jaringan IoT dapat dikelompokkan menjadi tiga kategori intensitas, yaitu **Trafik Intensitas Rendah**, **Trafik Intensitas Sedang**, dan **Trafik Intensitas Tinggi**.

## Tujuan

Tujuan dari program ini adalah:

1. Mengimplementasikan algoritma K-Means Clustering pada dataset trafik IoT.
2. Mengelompokkan data trafik jaringan IoT ke dalam tiga cluster berdasarkan intensitas trafik.
3. Membandingkan hasil clustering menggunakan metode jarak Euclidean, Manhattan, dan Minkowski.
4. Menampilkan jumlah data pada setiap cluster serta komposisi `Attack_type` terbanyak.
5. Membuat visualisasi hasil clustering agar pola pengelompokan data lebih mudah dipahami.
6. Membandingkan dua pendekatan penghentian iterasi, yaitu berdasarkan perubahan label cluster dan berdasarkan threshold perubahan centroid.

## Penjelasan Dataset

Dataset yang digunakan adalah **RT-IoT2022** dengan nama file:

```bash
RT_IOT2022.csv
```

Dataset ini berisi data trafik jaringan IoT. Pada program, data dibaca menggunakan library `pandas`. Untuk mempercepat proses komputasi, program menggunakan sampel sebanyak **5.000 data** apabila jumlah data asli lebih besar dari 5.000 baris.

Kolom `Attack_type` digunakan sebagai label asli untuk membantu membaca komposisi data pada setiap cluster. Namun, proses clustering tidak menggunakan kolom tersebut sebagai fitur utama, karena K-Means bekerja berdasarkan kemiripan nilai fitur numerik.

## Fitur yang Dipilih

Fitur yang digunakan dalam proses clustering adalah fitur numerik yang berkaitan dengan durasi aliran data, jumlah paket, kecepatan paket, rasio arah komunikasi, jumlah flag, payload, dan ukuran window. Fitur yang dipilih adalah sebagai berikut:

1. `flow_duration`
2. `fwd_pkts_tot`
3. `bwd_pkts_tot`
4. `fwd_data_pkts_tot`
5. `bwd_data_pkts_tot`
6. `fwd_pkts_per_sec`
7. `bwd_pkts_per_sec`
8. `flow_pkts_per_sec`
9. `down_up_ratio`
10. `flow_SYN_flag_count`
11. `flow_RST_flag_count`
12. `flow_ACK_flag_count`
13. `fwd_pkts_payload.tot`
14. `bwd_pkts_payload.tot`
15. `flow_pkts_payload.tot`
16. `payload_bytes_per_second`
17. `fwd_init_window_size`
18. `bwd_init_window_size`
19. `fwd_last_window_size`

Sebelum proses clustering dilakukan, data pada fitur tersebut dibersihkan dari nilai tak hingga (`inf` dan `-inf`), nilai kosong diisi dengan `0`, lalu data dinormalisasi menggunakan standardisasi agar setiap fitur memiliki skala yang seimbang.

## Metode yang Digunakan

### 1. K-Means Clustering

K-Means merupakan metode clustering yang bertujuan membagi data ke dalam sejumlah cluster berdasarkan kedekatan data terhadap centroid. Dalam program ini jumlah cluster ditetapkan sebanyak tiga, yaitu:

- Cluster trafik intensitas rendah
- Cluster trafik intensitas sedang
- Cluster trafik intensitas tinggi

### 2. Metode Jarak

Program menggunakan tiga metode jarak untuk membandingkan hasil clustering:

- **Euclidean Distance**: menghitung jarak lurus antara data dan centroid.
- **Manhattan Distance**: menghitung jarak berdasarkan jumlah selisih absolut antar fitur.
- **Minkowski Distance**: generalisasi dari Euclidean dan Manhattan, dengan nilai `p = 3`.

### 3. Penamaan Cluster

Cluster tidak langsung diberi nama berdasarkan nomor cluster. Program menghitung skor intensitas trafik dari beberapa fitur penting, yaitu:

- `flow_pkts_per_sec`
- `payload_bytes_per_second`
- `flow_pkts_payload.tot`
- `flow_SYN_flag_count`
- `flow_RST_flag_count`
- `flow_ACK_flag_count`

Rata-rata skor tersebut digunakan untuk mengurutkan cluster dari intensitas terendah sampai tertinggi. Setelah itu, cluster diberi nama:

- Trafik Intensitas Rendah
- Trafik Intensitas Sedang
- Trafik Intensitas Tinggi

## Struktur File

```bash
.
├── RT_IOT2022.csv
├── kmeans_iot_k_diawal.py
├── kmeans_iot_threshold.py
├── grafik_kmeans_k_diawal.png
└── grafik_kmeans_threshold.png
```

Keterangan:

- `RT_IOT2022.csv` adalah dataset utama.
- `kmeans_iot_k_diawal.py` adalah program K-Means dengan nilai K ditentukan sejak awal.
- `kmeans_iot_threshold.py` adalah program K-Means dengan batas penghentian berdasarkan threshold.
- `grafik_kmeans_k_diawal.png` adalah hasil visualisasi dari program K-Means dengan K di awal.
- `grafik_kmeans_threshold.png` adalah hasil visualisasi dari program K-Means dengan threshold.

## Library yang Dibutuhkan

Program ini menggunakan beberapa library Python berikut:

```python
pandas
numpy
matplotlib
```

Untuk menginstal library yang dibutuhkan, jalankan perintah berikut:

```bash
pip install pandas numpy matplotlib
```

## Cara Menggunakan Program

### 1. Siapkan File Dataset

Pastikan file dataset bernama `RT_IOT2022.csv` berada dalam folder yang sama dengan file Python.

Contoh struktur folder:

```bash
folder_project/
├── RT_IOT2022.csv
├── kmeans_iot_k_diawal.py
└── kmeans_iot_threshold.py
```

### 2. Jalankan Program K-Means dengan K di Awal

Gunakan perintah berikut:

```bash
python kmeans_iot_k_diawal.py
```

Program akan menampilkan informasi berupa:

- Nama dataset
- Metode jarak yang digunakan
- Jumlah cluster
- Jumlah data
- Jumlah iterasi
- Jumlah data pada setiap cluster
- Komposisi `Attack_type` terbanyak pada setiap cluster

Program juga akan menghasilkan file grafik:

```bash
grafik_kmeans_k_diawal.png
```

### 3. Jalankan Program K-Means dengan Threshold

Gunakan perintah berikut:

```bash
python kmeans_iot_threshold.py
```

Program akan menampilkan informasi berupa:

- Nama dataset
- Metode jarak yang digunakan
- Jumlah cluster
- Nilai threshold
- Jumlah data
- Nilai delta setiap iterasi
- Iterasi saat program berhenti
- Jumlah data pada setiap cluster
- Komposisi `Attack_type` terbanyak pada setiap cluster

Program juga akan menghasilkan file grafik:

```bash
grafik_kmeans_threshold.png
```

## Output Program

Output utama dari program adalah:

1. Informasi hasil clustering pada terminal.
2. Jumlah data pada masing-masing cluster.
3. Komposisi `Attack_type` terbanyak pada setiap cluster.
4. Grafik visualisasi hasil clustering.

Contoh kategori cluster yang dihasilkan:

```bash
Cluster 0 - Trafik Intensitas Rendah
Cluster 1 - Trafik Intensitas Sedang
Cluster 2 - Trafik Intensitas Tinggi
```

Nomor cluster dapat berbeda tergantung hasil perhitungan centroid. Oleh karena itu, program memberi nama cluster berdasarkan rata-rata skor intensitas trafik, bukan hanya berdasarkan nomor cluster.

## Kesimpulan

Program ini digunakan untuk melakukan pengelompokan trafik jaringan IoT menggunakan algoritma K-Means. Dengan menggunakan fitur-fitur numerik dari dataset RT-IoT2022, data dapat dikelompokkan menjadi tiga kategori intensitas trafik. Perbandingan metode jarak Euclidean, Manhattan, dan Minkowski membantu melihat pengaruh pemilihan metode jarak terhadap hasil clustering.

Dua pendekatan program yang digunakan, yaitu K-Means dengan K di awal dan K-Means dengan threshold, memberikan gambaran mengenai cara kerja proses iterasi pada algoritma K-Means. Hasil akhir program dapat membantu pengguna memahami pola trafik jaringan IoT serta melihat jenis trafik atau serangan yang dominan pada setiap cluster.

