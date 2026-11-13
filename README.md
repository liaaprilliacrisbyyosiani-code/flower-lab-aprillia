# Flower Lab — Aprillia

## Menjalankan secara lokal
1. Install Python 3.10 atau lebih baru.
2. Buka terminal di folder proyek.
3. Jalankan:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Browser akan membuka aplikasi Streamlit.

## Deploy ke Streamlit Community Cloud
1. Buat repository GitHub baru.
2. Upload `app.py` dan `requirements.txt` ke root repository.
3. Buka https://share.streamlit.io/ dan login dengan GitHub.
4. Pilih **Create app**, pilih repository, branch, dan file utama `app.py`.
5. Klik **Deploy**.
6. Setelah status aplikasi berjalan, salin URL Streamlit dan kumpulkan URL tersebut ke LMS.

## Catatan validitas
Aplikasi ini merupakan dashboard visual interaktif dengan data loss ilustratif. Ini tidak menjalankan training Flower secara langsung dan tidak terhubung ke Flower SuperGrid. Laporan Aprillia mencatat run nyata Flower SuperGrid ID `14714596137151743331`, status Completed, 1 server, 3 client virtual, 1 round, 3 hasil diterima, 0 failures.
