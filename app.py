import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model # pyright: ignore
import joblib
import time
import json
import os
from flask import Flask, render_template, Response

app = Flask(__name__)

# Load models on startup
try:
    model = load_model('adaptive_ids_lstm_model.h5')
    scaler = joblib.load('ids_data_scaler.pkl')
    print("[SYSTEM] LSTM Model and Scaler loaded successfully.")
except Exception as e:
    print(f"[ERROR] Could not load model/scaler. Details: {e}")
    model, scaler = None, None

def generate_traffic():
    if model is None or scaler is None:
        yield f"data: {json.dumps({'error': 'Model not loaded'})}\n\n"
        return

    # Load data
    try:
        live_traffic = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', skiprows=100000, nrows=200) 
        columns_to_drop = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack', 'Label', 'Dataset']
        features_only = live_traffic.drop(columns=[col for col in columns_to_drop if col in live_traffic.columns])
        expected_cols = scaler.feature_names_in_
        for col in expected_cols:
            if col not in features_only.columns:
                features_only[col] = 0.0
        features_only = features_only[expected_cols]
    except Exception as e:
        yield f"data: {json.dumps({'error': f'Data loading failed: {e}'})}\n\n"
        return

    for index, row in features_only.iterrows():
        single_packet = pd.DataFrame([row.values], columns=features_only.columns)
        scaled_packet = scaler.transform(single_packet)
        lstm_packet = np.expand_dims(scaled_packet, axis=2)
        prediction_prob = float(model.predict(lstm_packet, verbose=0)[0][0])
        
        is_attack = prediction_prob > 0.50
        status = "ALERT" if is_attack else "NORMAL"
        confidence = round(prediction_prob * 100, 2) if is_attack else round((1 - prediction_prob) * 100, 2)
        
        # Generic source/dest string for UI
        src_ip = f"192.168.1.{10 + (index % 50)}"
        dst_port = 80 if index % 3 == 0 else (443 if index % 2 == 0 else 22)
        
        packet_data = {
            "packet_id": index + 1,
            "status": status,
            "confidence": confidence,
            "details": f"{src_ip} -> port {dst_port}"
        }
        
        yield f"data: {json.dumps(packet_data)}\n\n"
        time.sleep(0.5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(generate_traffic(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
