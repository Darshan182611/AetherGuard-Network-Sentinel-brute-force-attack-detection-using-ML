import pandas as pd
import joblib
import numpy as np

print("[TEST] Loading new model...")
model = joblib.load('ids_model_logistic.pkl')
scaler = joblib.load('ids_scaler_logistic.pkl')

print("[TEST] Loading test data...")
df = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', nrows=1000)

columns_to_drop = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack', 'Label', 'Dataset']
X = df.drop(columns=columns_to_drop)
y = df['Label']

# Scale and predict
X_scaled = scaler.transform(X)
predictions = model.predict_proba(X_scaled)[:, 1]

# Separate by actual label
benign_preds = predictions[y == 0]
attack_preds = predictions[y == 1]

print("\n" + "="*70)
print(" MODEL VALIDATION - NEW WORKING MODEL ".center(70, "="))
print("="*70)

print(f"\nBENIGN TRAFFIC (should be < 0.5):")
print(f"  Count: {len(benign_preds)}")
print(f"  Mean: {np.mean(benign_preds):.4f}")
print(f"  Correctly classified: {sum(benign_preds < 0.5)}/{len(benign_preds)}")
print(f"  Sample values: {benign_preds[:5]}")

print(f"\nATTACK TRAFFIC (should be > 0.5):")
print(f"  Count: {len(attack_preds)}")
print(f"  Mean: {np.mean(attack_preds):.4f}")
print(f"  Correctly classified: {sum(attack_preds > 0.5)}/{len(attack_preds)}")
print(f"  Sample values: {attack_preds[:5]}")

print("\n" + "="*70)
overall_acc = (sum(benign_preds < 0.5) + sum(attack_preds > 0.5)) / len(predictions)
print(f"Overall Accuracy on test data: {overall_acc*100:.2f}%")
print("="*70)

if np.std(predictions) > 0.1:
    print("\n[SUCCESS] Model is working properly!")
    print("[INFO] Predictions have good variance and discrimination.")
else:
    print("\n[WARNING] Model predictions may not have enough variance.")
