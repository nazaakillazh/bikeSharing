# Bike sharing data analysis
Dashboard ini dibuat untuk menganalisis data peminjaman sepeda berdasarkan dataset day.csv dan hour.csv. Data ini mencakup tren peminjaman sepeda berdasarkan musim, cuaca, dan tanggal.

## Cara menjalankan kode:
### 1. Install library yang dibutuhkan
Sebelum menjalankan dashboard, pastikan sudah menginstall semua library yang diperlukan:
- Anaconda
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
- Command prompt
python -m venv myenv
    - Windows
        myenv\Scripts\activate
    - macOS and Linux
        source myenv/bin/activate
pip install -r requirements.txt
### 2. Jalankan dashboard
Gunakan perintah berikut untuk menjalankan streamlit:
"streamlit run dashboard/dashboard.py"

## Fitur dashboard:
- Tren penggunaan sepeda: Visualisasi jumlah pengguna sepeda sepanjang tahun.
- Pengaruh musim: Boxplot untuk melihat perbedaan peminjaman sepeda di berbagai musim.
- Pengaruh cuaca: Analisis bagaimana kondisi cuaca mempengaruhi jumlah peminjam sepeda.

## Struktur folder
submission
├───dashboard
│   ├───main_data.csv
│   ├───dashboard.py
├───data
│   ├───day.csv
│   ├───hour.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt