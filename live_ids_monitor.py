import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib
import time
import os

# --- 1. Load the "Brain" ---
print("[SYSTEM] Booting up Adaptive ML-IDS...")
try:
    model = load_model('adaptive_ids_lstm_model.h5')
    scaler = joblib.load('ids_data_scaler.pkl')
    print("[SYSTEM] LSTM Model and Scaler loaded successfully. \n")
except Exception as e:
    print(f"[ERROR] Could not load model/scaler. Ensure they are in the same folder. Details: {e}")
    exit()

# --- 2. Simulate Incoming Network Traffic ---
# In a real environment, this would read from /var/log/auth.log
# For our simulation, we will read a small chunk of your Kaggle dataset.
print("[SYSTEM] Connecting to network traffic stream...\n")
time.sleep(2)

# Load 50 random rows from the dataset to act as "live" incoming packets
# Replace 'NF-UQ-NIDS-v2.csv' if your file is named differently
live_traffic = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', skiprows=100000, nrows=200) 
# Note: We skip the first 100k rows so the model sees brand new data it hasn't trained on!

# We must drop the exact same columns we dropped during training in Phase 2
columns_to_drop = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack', 'Label', 'Dataset']
features_only = live_traffic.drop(columns=[col for col in columns_to_drop if col in live_traffic.columns])

# Ensure the DataFrame has the exact columns the scaler expects
expected_cols = scaler.feature_names_in_
for col in expected_cols:
    if col not in features_only.columns:
        features_only[col] = 0.0
features_only = features_only[expected_cols]

print("-" * 60)
print(" LIVE NETWORK MONITOR ACTIVE ".center(60, "="))
print("-" * 60)

# --- 3. The Real-Time Scanning Loop ---
# Initialize reporting variables
alerts = 0
normal_traffic = 0
all_predictions = []

# We process one connection at a time to simulate real-time monitoring
for index, row in features_only.iterrows():
    # 1. Format the single log entry into a 2D array
    single_packet = pd.DataFrame([row.values], columns=features_only.columns)
    
    # 2. Scale the data using the exact math from Phase 2
    scaled_packet = scaler.transform(single_packet)
    
    # 3. Reshape for the LSTM (samples, timesteps, features)
    lstm_packet = np.expand_dims(scaled_packet, axis=2)
    
    # 4. Ask the AI to predict (Verbose=0 hides the loading bar)
    prediction_prob = model.predict(lstm_packet, verbose=0)[0][0]
    
    # 5. Determine if it is an attack (Threshold > 50%)
    if prediction_prob > 0.50:
        threat_level = round(prediction_prob * 100, 2)
        print(f"[ 🚨 ALERT ] BRUTE-FORCE DETECTED! Confidence: {threat_level}% | Connection Blocked.")
        alerts += 1
        all_predictions.append({"packet": index + 1, "status": "ALERT", "confidence": threat_level})
    else:
        print(f"[ OK ] Normal Traffic Allowed.")
        normal_traffic += 1
        all_predictions.append({"packet": index + 1, "status": "NORMAL", "confidence": round((1 - prediction_prob) * 100, 2)})
    
    # Pause for half a second to simulate the flow of time
    time.sleep(0.5)

# --- 4. Display Monitoring Report ---
print("\n" + "=" * 60)
print(" MONITORING SESSION REPORT ".center(60, "="))
print("=" * 60)
print(f"\n[STATS] Session Statistics:")
print(f"   Total Packets Processed: {alerts + normal_traffic}")
print(f"   Normal Traffic: {normal_traffic} ({round((normal_traffic / (alerts + normal_traffic)) * 100, 1)}%)")
print(f"   Detected Alerts: {alerts} ({round((alerts / (alerts + normal_traffic)) * 100, 1)}%)")
print(f"   Detection Rate: {round((alerts / (alerts + normal_traffic)) * 100, 2)}%")

if alerts > 0:
    print(f"\n[ALERT] Alert Summary:")
    alert_packets = [p for p in all_predictions if p["status"] == "ALERT"]
    for alert in alert_packets:
        print(f"   - Packet #{alert['packet']}: {alert['confidence']}% confidence")
else:
    print(f"\n[OK] No Threats Detected - All traffic is safe!")

print("\n" + "=" * 60)
print("[SYSTEM] Monitoring session ended successfully.")
print("=" * 60)
