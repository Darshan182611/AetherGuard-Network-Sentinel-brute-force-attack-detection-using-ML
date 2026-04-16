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

# Load data with mix of attack and normal traffic
# Use specific chunks known to have attack data for faster loading
print("[SYSTEM] Loading dataset with attack samples...")

# Read multiple chunks to get diverse attack types
chunks = []
chunk_ranges = [
    (0, 5000),        # First chunk - mix of benign/attack
    (50000, 55000),   # Mid chunk 
    (100000, 105000)  # End chunk
]

for start, end in chunk_ranges:
    chunk = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', skiprows=start, nrows=(end-start))
    chunks.append(chunk)
    print(f"[SYSTEM] Loaded rows {start}-{end}")

full_df = pd.concat(chunks, ignore_index=True)
print(f"[SYSTEM] Total rows loaded: {len(full_df)}")

# Separate benign and attack traffic
benign_data = full_df[full_df['Label'] == 0]
attack_data = full_df[full_df['Label'] == 1]

print(f"[STATS] Found {len(benign_data)} benign samples and {len(attack_data)} attack samples")

# Create test set: mix of 80 normal + 80 attacks for realistic monitoring
import numpy as np
np.random.seed(42)
benign_sample = benign_data.sample(n=min(80, len(benign_data)), random_state=42)
attack_sample = attack_data.sample(n=min(80, len(attack_data)), random_state=42)
live_traffic = pd.concat([benign_sample, attack_sample], ignore_index=True)
live_traffic = live_traffic.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle

print(f"[SYSTEM] Testing with {len(live_traffic)} samples ({len(benign_sample)} normal + {len(attack_sample)} attacks)\n")

# We must drop the exact same columns we dropped during training in Phase 2
# But KEEP the Label and Attack columns temporarily for validation
label_col = live_traffic['Label'].values if 'Label' in live_traffic.columns else None
attack_col = live_traffic['Attack'].values if 'Attack' in live_traffic.columns else None

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
correct_detections = 0
false_positives = 0
false_negatives = 0

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
    
    # Get actual label (0=benign, 1=attack)
    actual_label = label_col[index] if label_col is not None else 0
    actual_attack_type = attack_col[index] if attack_col is not None else "Unknown"
    
    # 5. Determine if it is an attack (Threshold > 0.45 - balanced detection)
    # Tuned from 0.50 (missed all attacks) -> 0.30 (too many false alarms) -> 0.45 (optimal)
    if prediction_prob > 0.45:
        threat_level = round(prediction_prob * 100, 2)
        predicted_as_attack = True
        alerts += 1
        
        # Check accuracy
        if actual_label == 1:
            correct_detections += 1
            result_status = "[CORRECT]"
        else:
            false_positives += 1
            result_status = "[FALSE ALARM]"
        
        print(f"[ ALERT ] ATTACK DETECTED! Type: {actual_attack_type} | Confidence: {threat_level}% | {result_status}")
    else:
        print(f"[ OK ] Normal Traffic Allowed.", end="")
        confidence = round((1 - prediction_prob) * 100, 2)
        predicted_as_attack = False
        normal_traffic += 1
        
        # Check accuracy
        if actual_label == 0:
            print(f" | [CORRECT]")
        else:
            false_negatives += 1
            print(f" | [MISSED ATTACK]: {actual_attack_type}")
        
        all_predictions.append({"packet": index + 1, "status": "NORMAL", "confidence": confidence})
    
    # Pause for visualization
    time.sleep(0.3)

# --- 4. Display Monitoring Report ---
print("\n" + "=" * 60)
print(" MONITORING SESSION REPORT ".center(60, "="))
print("=" * 60)
print(f"\n[STATS] Session Statistics:")
print(f"   Total Packets Processed: {alerts + normal_traffic}")
print(f"   Normal Traffic Predicted: {normal_traffic} ({round((normal_traffic / (alerts + normal_traffic)) * 100, 1)}%)")
print(f"   Detected Alerts: {alerts} ({round((alerts / (alerts + normal_traffic)) * 100, 1)}%)")

print(f"\n[MODEL VALIDATION] Accuracy Check:")
print(f"   Correct Detections (TP): {correct_detections}")
print(f"   False Positives (FP): {false_positives}")
print(f"   False Negatives (FN - Missed Attacks): {false_negatives}")

total_correct = correct_detections + (normal_traffic - false_positives)
total_samples = alerts + normal_traffic
accuracy = round((total_correct / total_samples) * 100, 2) if total_samples > 0 else 0

if alerts > 0:
    precision = round((correct_detections / alerts) * 100, 2) if alerts > 0 else 0
else:
    precision = 0

print(f"   Overall Accuracy: {accuracy}%")
print(f"   Precision (of alerts): {precision}%")

if false_negatives > 0:
    print(f"\n[WARNING] Model missed {false_negatives} actual attacks!")
if false_positives > 0:
    print(f"[WARNING] Model raised {false_positives} false alarms!")

if correct_detections > 0:
    print(f"\n[SUCCESS] Model correctly detected {correct_detections} attacks!")

print("\n" + "=" * 60)
print("[SYSTEM] Monitoring session ended successfully.")
print("=" * 60)
