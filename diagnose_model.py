import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib

print("[SYSTEM] Loading model and scaler...")
model = load_model('adaptive_ids_lstm_model.h5')
scaler = joblib.load('ids_data_scaler.pkl')

# Load just attack samples to see what predictions the model makes
print("[SYSTEM] Loading attack samples...")
full_df = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', nrows=5000)
attack_data = full_df[full_df['Label'] == 1].head(20)

print(f"\n[DIAGNOSIS] Testing model on {len(attack_data)} attack samples\n")
print("Attack Type".ljust(20), "Model Output".ljust(15), "0.5 detect".ljust(12), "0.3 detect".ljust(12), "0.1 detect")
print("-" * 75)

columns_to_drop = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack', 'Label', 'Dataset']
expected_cols = scaler.feature_names_in_

predictions = []

for idx, (index, row) in enumerate(attack_data.iterrows()):
    # Drop non-feature columns from this row
    row_dict = row.to_dict()
    for col in columns_to_drop:
        row_dict.pop(col, None)
    
    # Create dataframe with just the row data
    features_row = pd.DataFrame([row_dict])
    
    # Ensure all expected columns are present
    for col in expected_cols:
        if col not in features_row.columns:
            features_row[col] = 0.0
    
    # Select only expected columns in correct order
    features_row = features_row[expected_cols]
    
    scaled_packet = scaler.transform(features_row)
    lstm_packet = np.expand_dims(scaled_packet, axis=2)
    prediction_prob = float(model.predict(lstm_packet, verbose=0)[0][0])
    
    attack_type = row.get('Attack', 'Unknown')
    detect_05 = "ALERT" if prediction_prob > 0.5 else "MISS"
    detect_03 = "ALERT" if prediction_prob > 0.3 else "MISS"
    detect_01 = "ALERT" if prediction_prob > 0.1 else "MISS"
    
    predictions.append(prediction_prob)
    print(f"{str(attack_type)[:20].ljust(20)} {prediction_prob:.6f}".ljust(15), detect_05.ljust(12), detect_03.ljust(12), detect_01)

print("\n" + "=" * 75)
print(f"[STATISTICS]")
print(f"Mean prediction: {np.mean(predictions):.6f}")
print(f"Std deviation: {np.std(predictions):.6f}")
print(f"Min prediction: {np.min(predictions):.6f}")
print(f"Max prediction: {np.max(predictions):.6f}")
print(f"\nDetection rates at different thresholds:")
print(f"  Threshold 0.5: {sum(p > 0.5 for p in predictions)}/{len(predictions)} detected")
print(f"  Threshold 0.3: {sum(p > 0.3 for p in predictions)}/{len(predictions)} detected")
print(f"  Threshold 0.1: {sum(p > 0.1 for p in predictions)}/{len(predictions)} detected")
print(f"  Threshold 0.05: {sum(p > 0.05 for p in predictions)}/{len(predictions)} detected")
print(f"  Threshold 0.01: {sum(p > 0.01 for p in predictions)}/{len(predictions)} detected")
print("=" * 75)
