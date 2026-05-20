import joblib  # manggil file .pkl
import numpy as np
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key_personality"

try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    print("Model dan Scaler berhasil dimuat.")
except Exception as e:
    print(f"Error saat memuat file: {e}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        try:
            time_spent_alone = int(request.form["time_spent_alone"])
            stage_fear = request.form["stage_fear"] == "true"
            drained_after_socializing = (
                request.form["drained_after_socializing"] == "true"
            )
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

            fitur_scaled = scaler.transform(fitur_raw)
            prediksi = model.predict(fitur_scaled)
            hasil_angka = int(prediksi[0])

            # Mengirimkan tipe kepribadian sebagai kategori flash
            if hasil_angka == 0:
                flash("You are likely an Extrovert!", "extrovert")
            else:
                flash("You are likely an Introvert!", "introvert")

        except Exception as e:
            flash(f"Kesalahan Sistem: {str(e)}", "error")

        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
