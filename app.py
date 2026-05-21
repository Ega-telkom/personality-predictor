import joblib  # manggil file .pkl
import numpy as np
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key_personality"

# --- LOAD MODELS & SCALERS SAFELY ---
# It is important to have separate models/scalers for each feature 
# because they expect different feature column structures.
try:
    model_personality = joblib.load("model_personality.pkl")  # Atau renamed ke model_personality.pkl
    scaler_personality = joblib.load("scaler_personality.pkl")
    print("Personality Model dan Scaler berhasil dimuat.")
except Exception as e:
    print(f"Error saat memuat file Personality ML: {e}")

try:
    # Menghindari bentrok matrix columns, gunakan file pkl terpisah untuk stunting
    model_stunting = joblib.load("model_stunting.pkl") 
    scaler_stunting = joblib.load("scaler_stunting.pkl")
    print("Stunting Model dan Scaler berhasil dimuat.")
except Exception as e:
    print(f"Error saat memuat file Stunting ML: {e}")

# --- ROUTES AND CONTROL LOGIC ---
@app.route("/")
def home():
    """Main dashboard panel portal hub screen."""
    return render_template("index.html")

@app.route('/personality')
def personality_page():
    """Renders the semantic multi-page Personality quiz wizard."""
    return render_template('index-personality.html')

@app.route('/stunting')
def stunting_page():
    """Renders the semantic multi-page Stunting evaluation form."""
    return render_template('index-stunting.html')

@app.route("/predict-personality", methods=["POST"])
def predict_personality():
    if request.method == "POST":
        try:
            time_spent_alone = int(request.form["time_spent_alone"])
            stage_fear = request.form["stage_fear"] == "true"
            drained_after_socializing = request.form["drained_after_socializing"] == "true"
            social_event_attendance = int(request.form["social_event_attendance"])
            going_outside = int(request.form["going_outside"])
            friends_circle_size = int(request.form["friends_circle_size"])
            post_frequency = int(request.form["post_frequency"])

            fitur_raw = np.array(
                [
                    [
                        time_spent_alone,
                        1 if stage_fear else 0,
                        social_event_attendance,
                        going_outside,
                        1 if drained_after_socializing else 0,
                        friends_circle_size,
                        post_frequency,
                    ]
                ]
            )

            fitur_scaled = scaler_personality.transform(fitur_raw)
            prediksi = model_personality.predict(fitur_scaled)
            hasil_angka = int(prediksi[0])

            # Mengirimkan tipe kepribadian sebagai kategori flash
            if hasil_angka == 0:
                flash("You are likely an Extrovert!", "extrovert")
            else:
                flash("You are likely an Introvert!", "introvert")

        except Exception as e:
            flash(f"Kesalahan Sistem Personality: {str(e)}", "error")

    return redirect(url_for('personality_page'))


@app.route('/predict-stunting', methods=['POST'])
def predict_stunting():
    if request.method == 'POST':
        try:
            # Mengambil data dari form wizard stunting
            umur = float(request.form['umur'])
            jk_input = request.form['jenis_kelamin']
            tinggi = float(request.form['tinggi'])

            # Konversi Jenis Kelamin (laki-laki = 1, perempuan = 0)
            jk = 1 if jk_input == 'laki-laki' else 0

            # Susun fitur dalam bentuk array 2D
            fitur_raw = np.array([[umur, jk, tinggi]])
                    
            # Scaling menggunakan scaler khusus data stunting
            fitur_scaled = scaler_stunting.transform(fitur_raw)
            
            # Melakukan prediksi
            prediksi = model_stunting.predict(fitur_scaled)
            angka_hasil = int(prediksi[0])

            # Mapping Label Encoder hasil training
            status_map = {
                0: "Normal",
                1: "Sangat Pendek",
                2: "Pendek",
                3: "Tinggi"
            }
            
            hasil_teks = status_map.get(angka_hasil, f"Kode: {angka_hasil}")
            
            # Mengirimkan response via flash message terstruktur agar
            # UI transisi step-by-step bekerja dengan elegan tanpa refresh halaman total
            flash(f"{hasil_teks}|{angka_hasil}", "stunting_result")
        
        except Exception as e:
            flash(f"Kesalahan Sistem Stunting: {str(e)}", "stunting_error")
            
    return redirect(url_for('stunting_page'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
