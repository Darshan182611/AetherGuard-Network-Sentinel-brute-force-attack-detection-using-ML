import pandas as pd
import numpy as np
import joblib
import time
import json
import os
from flask import Flask, render_template, Response

app = Flask(__name__)

# Load models on startup
try:
    # Load the new working Logistic Regression model
    model = joblib.load('ids_model_logistic.pkl')
    scaler = joblib.load('ids_scaler_logistic.pkl')
    print("[SYSTEM] Working IDS Model (Logistic Regression) and Scaler loaded successfully.")
except Exception as e:
    print(f"[ERROR] Could not load model/scaler. Details: {e}")
    model, scaler = None, None

def generate_traffic():
    if model is None or scaler is None:
        yield f"data: {json.dumps({'error': 'Model not loaded'})}\n\n"
        return

    # Load data with MIXED attack and benign samples
    try:
        print("[SYSTEM] Loading dataset with mixed attack and benign traffic...")
        
        # Load data efficiently - read first 50K rows directly at once
        print("[SYSTEM] Reading first 50K rows from dataset...")
        full_df = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', nrows=50000)
        
        # Separate benign and attack traffic
        benign_data = full_df[full_df['Label'] == 0]
        attack_data = full_df[full_df['Label'] == 1]
        
        print(f"[STATS] Found {len(benign_data)} benign and {len(attack_data)} attack samples")
        
        # Create mixed dataset: Use large sample sizes matching training data
        np.random.seed(42)
        benign_sample = benign_data.sample(n=min(8000, len(benign_data)), random_state=42)
        attack_sample = attack_data.sample(n=min(16000, len(attack_data)), random_state=42)
        live_traffic = pd.concat([benign_sample, attack_sample], ignore_index=True)
        live_traffic = live_traffic.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle
        
        print(f"[SYSTEM] Testing with {len(live_traffic)} mixed samples ({len(benign_sample)} benign + {len(attack_sample)} attacks)\n")
        
        # Keep labels for validation
        label_col = live_traffic['Label'].values if 'Label' in live_traffic.columns else None
        attack_col = live_traffic['Attack'].values if 'Attack' in live_traffic.columns else None
        
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

    # Initialize counters
    alerts = 0
    normal_count = 0
    
    for index, row in features_only.iterrows():
        single_packet = pd.DataFrame([row.values], columns=features_only.columns)
        scaled_packet = scaler.transform(single_packet)
        
        # Use sklearn model - get probability of attack (class 1)
        prediction_prob = float(model.predict_proba(scaled_packet)[0][1])
        
        # Use standard threshold of 0.5
        is_attack = prediction_prob > 0.5
        status = "ALERT" if is_attack else "NORMAL"
        
        if is_attack:
            alerts += 1
            confidence = round(prediction_prob * 100, 2)
        else:
            normal_count += 1
            confidence = round((1 - prediction_prob) * 100, 2)
        
        # Get actual label if available
        actual_attack_type = attack_col[index] if attack_col is not None else "Unknown"
        actual_is_attack = label_col[index] if label_col is not None else 0
        
        # Generic source/dest string for UI
        src_ip = f"192.168.1.{10 + (index % 50)}"
        dst_port = 80 if index % 3 == 0 else (443 if index % 2 == 0 else 22)
        
        # Validation: Check if prediction matches actual label
        prediction_correct = (is_attack and actual_is_attack == 1) or (not is_attack and actual_is_attack == 0)
        validation_status = "CORRECT" if prediction_correct else "MISMATCH"
        
        packet_data = {
            "packet_id": index + 1,
            "status": status,
            "confidence": confidence,
            "details": f"{src_ip} -> port {dst_port}",
            "attack_type": str(actual_attack_type),
            "validation": validation_status,
            "actual_label": "ATTACK" if actual_is_attack == 1 else "BENIGN"
        }
        
        yield f"data: {json.dumps(packet_data)}\n\n"
        time.sleep(0.3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(generate_traffic(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
