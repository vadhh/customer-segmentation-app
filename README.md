# Customer Segmentation App

Aplikasi dashboard sederhana untuk melakukan segmentasi pelanggan menggunakan model K-Means dan menampilkan hasil prediksi beserta strategi bisnis per-segmen. Aplikasi dibuat dengan Streamlit, visualisasi menggunakan Plotly, dan model disimpan sebagai file `joblib`.

**Fitur utama**
- Prediksi segmen pelanggan (input: TotalQuantity, AvgUnitPrice, AvgTransactionValue).
- Visualisasi 3D cluster menggunakan Plotly.
- Randomizer input (pilihan general dan per-cluster) untuk mudah menguji skenario.
- Panel strategi bisnis lengkap per cluster ditampilkan setelah prediksi.

**Requirements (disarankan)**
- Python 3.8+
- streamlit
- pandas
- numpy
- scikit-learn
- joblib
- plotly

Contoh instalasi cepat:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install streamlit pandas numpy scikit-learn joblib plotly
```

Atau (jika Anda membuat `requirements.txt`):

```bash
pip install -r requirements.txt
```

**Cara menjalankan**

Jalankan aplikasi Streamlit dari root proyek:

```bash
streamlit run /home/stardhoom/customer-segmentation-app/app.py
```

Akses aplikasi pada URL yang ditampilkan (biasanya `http://localhost:8501`).

**File penting dalam repo**
- `app.py` : Aplikasi Streamlit utama (UI, randomizer, prediksi, visualisasi, strategi).
- `kmeans_model.joblib` : (tidak termasuk di repo) file model KMeans yang sudah dilatih.
- `scaler.joblib` : (tidak termasuk di repo) scaler yang digunakan saat training.
- `cluster_data.csv` : (opsional) data sample untuk visualisasi cluster.

Jika model (`.joblib`) tidak ditemukan, aplikasi akan menampilkan pesan error. Letakkan `kmeans_model.joblib` dan `scaler.joblib` di folder yang sama dengan `app.py`.

**Catatan tentang input & randomizer**
- Input utama: `TotalQuantity`, `AvgUnitPrice`, `AvgTransactionValue`.
- Terdapat tombol Randomizer umum dan tombol randomizer per-cluster (Big Spender, Frugal, Regular, Bulk Buyer) untuk menghasilkan skenario uji.
- Rentang nilai randomizer disesuaikan agar realistis.

**Strategi bisnis per-cluster**
Aplikasi menampilkan strategi singkat dan lengkap tiap cluster di bawah hasil prediksi (expandable). Strategi mencakup: ringkasan persona, taktik jangka pendek, taktik jangka panjang, channel komunikasi, KPI yang harus dipantau, dan contoh kampanye.

**Saran penggunaan & pengembangan**
- Untuk eksperimen, gunakan randomizer per-cluster untuk A/B test ide kampanye.
- Tambahkan `requirements.txt` atau gunakan environment manager (conda/venv) untuk reproducibility.
- Jika ingin mengemaskini persona atau strategi, edit `app.py` bagian `personas` dan `strategies`.

**Ingin saya bantu lagi?**
- Tambahkan `requirements.txt` otomatis.
- Simpan strategi ke file `strategies.md` atau tombol ekspor ke PDF.
- Menambahkan endpoint API untuk integrasi B2B.

---


