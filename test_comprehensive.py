import pandas as pd
import numpy as np
import joblib
import sys

print("="*70)
print(" COMPREHENSIVE END-TO-END MODEL TEST ".center(70, "="))
print("="*70)

try:
    # Load the newly trained model
    print("\n[TEST] Loading new model from saved files...")
    model = joblib.load('ids_model_logistic.pkl')
    scaler = joblib.load('ids_scaler_logistic.pkl')
    print("[SUCCESS] New model and scaler loaded!")
    
    # Load test data
    print("\n[TEST] Loading test data...")
    df = pd.read_csv('../archive/NF-UQ-NIDS-v2.csv', nrows=1000)
    
    # Prepare features
    columns_to_drop = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack', 'Label', 'Dataset']
    X = df.drop(columns=columns_to_drop)
    y = df['Label'].values
    
    # Scale data
    X_scaled = scaler.transform(X)
    
    # Get predictions
    predictions = model.predict_proba(X_scaled)[:, 1]
    predicted_labels = model.predict(X_scaled)
    
    # Separate by actual class
    benign_mask = y == 0
    attack_mask = y == 1
    
    benign_pred = predictions[benign_mask]
    attack_pred = predictions[attack_mask]
    
    print(f"\n[TEST] Prediction Statistics:")
    print(f"  Total samples tested: {len(predictions)}")
    print(f"  Benign samples: {benign_mask.sum()}")
    print(f"  Attack samples: {attack_mask.sum()}")
    
    # Test benign traffic
    print(f"\n[BENIGN TRAFFIC TEST]")
    print(f"  Predictions < 0.5: {(benign_pred < 0.5).sum()}/{len(benign_pred)}")
    print(f"  Accuracy: {(benign_pred < 0.5).sum()/len(benign_pred)*100:.2f}%")
    print(f"  Mean prediction: {benign_pred.mean():.4f}")
    print(f"  Std deviation: {benign_pred.std():.4f}")
    print(f"  Min: {benign_pred.min():.4f}, Max: {benign_pred.max():.4f}")
    
    # Test attack traffic
    print(f"\n[ATTACK TRAFFIC TEST]")
    print(f"  Predictions > 0.5: {(attack_pred > 0.5).sum()}/{len(attack_pred)}")
    print(f"  Accuracy: {(attack_pred > 0.5).sum()/len(attack_pred)*100:.2f}%")
    print(f"  Mean prediction: {attack_pred.mean():.4f}")
    print(f"  Std deviation: {attack_pred.std():.4f}")
    print(f"  Min: {attack_pred.min():.4f}, Max: {attack_pred.max():.4f}")
    
    # Overall accuracy
    accuracy = (predicted_labels == y).sum() / len(y) * 100
    print(f"\n[OVERALL TEST]")
    print(f"  Accuracy: {accuracy:.2f}%")
    
    # Simulate Flask app prediction flow
    print(f"\n[FLASK SIMULATION TEST]")
    print(f"  Testing 10 random samples...")
    
    sample_indices = np.random.choice(len(X_scaled), 10, replace=False)
    for i, idx in enumerate(sample_indices, 1):
        pred_prob = float(model.predict_proba(X_scaled[idx:idx+1])[0][1])
        is_attack = pred_prob > 0.5
        actual_label = "ATTACK" if y[idx] == 1 else "BENIGN"
        predicted_label = "ATTACK" if is_attack else "BENIGN"
        status = "✓" if (predicted_label == actual_label) else "✗"
        print(f"  [{i:2d}] Actual: {actual_label:6} | Predicted: {predicted_label:6} | Prob: {pred_prob:.4f} {status}")
    
    print(f"\n[VARIANCE TEST]")
    print(f"  Prediction std deviation: {predictions.std():.6f}")
    if predictions.std() > 0.1:
        print(f"  ✓ Model has good variance (not stuck)")
    else:
        print(f"  ✗ WARNING: Model predictions have low variance")
    
    print(f"\n[DISCRIMINATION TEST]")
    print(f"  Benign mean: {benign_pred.mean():.4f}")
    print(f"  Attack mean: {attack_pred.mean():.4f}")
    print(f"  Separation: {(attack_pred.mean() - benign_pred.mean()):.4f}")
    if (attack_pred.mean() - benign_pred.mean()) > 0.3:
        print(f"  ✓ Models shows excellent class separation")
    else:
        print(f"  ✗ WARNING: Weak class separation")
    
    print("\n" + "="*70)
    print(" ALL TESTS COMPLETED SUCCESSFULLY ".center(70, "="))
    print("="*70)
    
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
