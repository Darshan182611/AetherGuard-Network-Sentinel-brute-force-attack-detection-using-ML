import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib
import warnings
warnings.filterwarnings('ignore')

print("[SYSTEM] Loading model and scaler...")
model = load_model('adaptive_ids_lstm_model.h5')
scaler = joblib.load('ids_data_scaler.pkl')

print("[SYSTEM] Loading dataset...")
full_df = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', nrows=10000)

# Separate benign and attack
benign_data = full_df[full_df['Label'] == 0]
attack_data = full_df[full_df['Label'] == 1]

print(f"[STATS] Benign: {len(benign_data)}, Attack: {len(attack_data)}\n")

columns_to_drop = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack', 'Label', 'Dataset']
expected_cols = scaler.feature_names_in_

def get_predictions(data, label_type, sample_size=50):
    """Get predictions for a dataset"""
    data_sample = data.sample(n=min(sample_size, len(data)), random_state=42)
    predictions = []
    
    for idx, (index, row) in enumerate(data_sample.iterrows()):
        row_dict = row.to_dict()
        for col in columns_to_drop:
            row_dict.pop(col, None)
        
        features_row = pd.DataFrame([row_dict])
        for col in expected_cols:
            if col not in features_row.columns:
                features_row[col] = 0.0
        
        features_row = features_row[expected_cols]
        scaled_packet = scaler.transform(features_row)
        lstm_packet = np.expand_dims(scaled_packet, axis=2)
        prediction_prob = float(model.predict(lstm_packet, verbose=0)[0][0])
        predictions.append(prediction_prob)
        
        if (idx + 1) % 10 == 0:
            print(f"  {label_type}: Processed {idx + 1}/{sample_size}")
    
    return np.array(predictions)

print("[DIAGNOSIS] Getting predictions for BENIGN traffic...")
benign_preds = get_predictions(benign_data, "BENIGN", 50)

print("\n[DIAGNOSIS] Getting predictions for ATTACK traffic...")
attack_preds = get_predictions(attack_data, "ATTACK", 50)

print("\n" + "="*80)
print(" MODEL OUTPUT ANALYSIS ".center(80, "="))
print("="*80)

print("\nBENIGN TRAFFIC PREDICTIONS:")
print(f"  Mean:   {np.mean(benign_preds):.6f}")
print(f"  Median: {np.median(benign_preds):.6f}")
print(f"  Std:    {np.std(benign_preds):.6f}")
print(f"  Min:    {np.min(benign_preds):.6f}")
print(f"  Max:    {np.max(benign_preds):.6f}")
print(f"  Q1:     {np.percentile(benign_preds, 25):.6f}")
print(f"  Q3:     {np.percentile(benign_preds, 75):.6f}")

print("\nATTACK TRAFFIC PREDICTIONS:")
print(f"  Mean:   {np.mean(attack_preds):.6f}")
print(f"  Median: {np.median(attack_preds):.6f}")
print(f"  Std:    {np.std(attack_preds):.6f}")
print(f"  Min:    {np.min(attack_preds):.6f}")
print(f"  Max:    {np.max(attack_preds):.6f}")
print(f"  Q1:     {np.percentile(attack_preds, 25):.6f}")
print(f"  Q3:     {np.percentile(attack_preds, 75):.6f}")

# Calculate optimal threshold
benign_mean = np.mean(benign_preds)
attack_mean = np.mean(attack_preds)
optimal_threshold = (benign_mean + attack_mean) / 2

print("\n" + "="*80)
print("THRESHOLD RECOMMENDATIONS:")
print("="*80)
print(f"Benign mean:     {benign_mean:.6f}")
print(f"Attack mean:     {attack_mean:.6f}")
print(f"Optimal threshold: {optimal_threshold:.6f}")
print(f"Current threshold: 0.45")

# Check overlap
benign_below_045 = sum(benign_preds < 0.45)
attack_above_045 = sum(attack_preds > 0.45)

print(f"\nWith threshold 0.45:")
print(f"  Benign detected as benign: {len(benign_preds) - benign_below_045}/{len(benign_preds)}")
print(f"  Attack detected as attack: {attack_above_045}/{len(attack_preds)}")

# Try different thresholds
print("\n" + "="*80)
print("THRESHOLD TESTING:")
print("="*80)

for threshold in np.arange(0.0, 1.0, 0.1):
    benign_correct = sum(benign_preds < threshold)
    attack_correct = sum(attack_preds >= threshold)
    accuracy = (benign_correct + attack_correct) / (len(benign_preds) + len(attack_preds))
    print(f"Threshold {threshold:.1f}: Benign correct={benign_correct}/{len(benign_preds)}, Attack correct={attack_correct}/{len(attack_preds)}, Accuracy={accuracy:.1f}%")

print("\n" + "="*80)

# Check if model is broken
if np.std(benign_preds) < 0.001 and np.std(attack_preds) < 0.001:
    print("[WARNING] MODEL APPEARS BROKEN - NO VARIANCE IN PREDICTIONS!")
    print("[INFO] Benign and attack outputs are identical. Model is not discriminative.")
    print("[SOLUTION] Need to retrain model or fix feature engineering.")
else:
    print("[OK] Model shows variance in predictions.")
