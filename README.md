# personality-predictor
Pemprediksi kepribadian

## Reproduksi
Agar sistemmu tidak berantakan, maka buat lingkungan terisolasi terlebih dahulu.
```sh
python3 -m venv venv
```
Lalu "aktifkan" lingkungan terisolasi tersebut.
Untuk Linux/MacOS/*BSD/Mirip-UNIX:
```sh
source venv/bin/activate
```
Untuk Microsoft® Windows®:
```sh
venv\Scripts\activate.bat
```
Pasang keperluan website:
```sh
pip install -r requirements.txt
```
Terakhir, jalankan website. Website akan berada dalam port `5000` dalam mode awakutu:
```sh
python app.py
```