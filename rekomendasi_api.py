from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Load model dan encoder
MODEL_PATH = 'rekomendasi_rf_model.joblib'
ENCODER_PATH = 'rekomendasi_labelencoders.joblib'
TARGET_ENCODER_PATH = 'rekomendasi_targetencoder.joblib'
DATASET_PATH = 'dataset/Book3.csv'

app = Flask(__name__)

# Load model dan encoder
model = joblib.load(MODEL_PATH)
le_dict = joblib.load(ENCODER_PATH)
target_encoder = joblib.load(TARGET_ENCODER_PATH)
df = pd.read_csv(DATASET_PATH, sep=';')

# Bersihkan spasi
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

fitur_cols = [
    "Intensitas Cahaya (Kategori)",
    "Intensitas Air (Kategori)",
    "Cara Penyiraman (Frekuensi)",
    "Konsep Utama Taman",
    "Ukuran Taman yang Cocok (Kategori)",
    "Lokasi Penanaman (Indoor/Outdoor)",
]


@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    # ==========================
    # Ambil input user
    # ==========================
    input_user_text = {}

    for col in fitur_cols:
        input_user_text[col] = data.get(col, "").strip()

    # ==========================
    # Validasi input
    # ==========================
    for col in fitur_cols:

        if input_user_text[col] == "":
            return jsonify({
                "error": f"Input untuk '{col}' tidak boleh kosong."
            }), 400

        if input_user_text[col] not in le_dict[col].classes_:
            return jsonify({
                "error": f"Input '{input_user_text[col]}' untuk '{col}' tidak valid.",
                "pilihan": list(le_dict[col].classes_)
            }), 400

    # ==========================
    # Encode input
    # ==========================
    input_encoded = {}

    try:
        for col in fitur_cols:
            input_encoded[col] = le_dict[col].transform(
                [input_user_text[col]]
            )[0]

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

    input_df = pd.DataFrame([input_encoded])

    # ==========================
    # Prediksi
    # ==========================
    try:
        proba = model.predict_proba(input_df)[0]

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    top3_index = proba.argsort()[-3:][::-1]

    top_types = []

    for idx in top3_index:

        tipe = target_encoder.inverse_transform([idx])[0]

        persen = round(float(proba[idx]) * 100, 2)

        top_types.append({
            "nama": tipe,
            "persen": persen
        })

    # ==========================
    # Ambil 5 tanaman tiap tipe
    # ==========================
    rekomendasi = []

    for tipe_info in top_types:

        tipe = tipe_info["nama"]

        tanaman_df = df[
            df["Tipe Utama Tanaman"] == tipe
        ].copy()

        skor = []

        for _, row in tanaman_df.iterrows():

            cocok = 0

            for col in fitur_cols:
                if row[col] == input_user_text[col]:
                    cocok += 1

            skor.append(cocok)

        tanaman_df["Skor"] = skor

        tanaman_df = tanaman_df.sort_values(
            by="Skor",
            ascending=False
        )

        top5 = tanaman_df.head(5)

        daftar_tanaman = []

        for _, row in top5.iterrows():

            daftar_tanaman.append({
                "nama": row["Nama Tanaman"],
                "skor": int(row["Skor"])
            })

        rekomendasi.append({
            "tipe": tipe,
            "persen": tipe_info["persen"],
            "tanaman": daftar_tanaman
        })

    return jsonify({
        "rekomendasi": rekomendasi
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
