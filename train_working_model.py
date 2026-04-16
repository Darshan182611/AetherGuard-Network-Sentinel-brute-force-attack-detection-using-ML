import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import warnings
import sys

warnings.filterwarnings('ignore')

print("="*70)
print(" IDS MODEL RETRAINING - 50K+ DATASET ".center(70, "="))
print("="*70)

try:
    # Load the full dataset with proper error handling
    print("\n[DATA] Loading dataset...")
    csv_path = '../archive/NF-UQ-NIDS-v2.csv'
    
    # Try to load with nrows specified first to get 50K
    try:
        df = pd.read_csv(csv_path, nrows=50000)
        print(f"[DATA] Successfully loaded 50,000 rows")
    except Exception as e:
        print(f"[ERROR] Failed to load with nrows: {e}")
        print("[DATA] Attempting to load entire dataset...")
        df = pd.read_csv(csv_path)
        print(f"[DATA] Loaded {len(df)} total rows from CSV")
    
    print(f"[DATA] Dataset shape: {df.shape}")
    print(f"[DATA] Columns: {list(df.columns)[:5]}... (showing first 5)")
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"[WARNING] Found {missing} missing values - removing rows with NaN...")
        df = df.dropna()
        print(f"[DATA] Shape after removing NaN: {df.shape}")
    
    # Get features and labels
    print("\n[PREPROCESS] Extracting features and labels...")
    columns_to_drop = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'Attack', 'Label', 'Dataset']
    
    # Verify columns exist
    for col in columns_to_drop:
        if col not in df.columns and col != 'Label':
            print(f"[WARNING] Column '{col}' not found, skipping...")
            columns_to_drop.remove(col)
    
    # Drop unnecessary columns
    X = df.drop(columns=columns_to_drop)
    y = df['Label'].values  # 0 = benign, 1 = attack
    
    print(f"[PREPROCESS] Feature matrix shape: {X.shape}")
    print(f"[PREPROCESS] Features: {X.shape[1]} columns")
    
    # Check label distribution
    unique_labels = np.unique(y)
    print(f"\n[PREPROCESS] Class distribution:")
    for label in unique_labels:
        count = np.sum(y == label)
        pct = (count / len(y)) * 100
        label_name = "BENIGN" if label == 0 else "ATTACK"
        print(f"  {label_name} (label={label}): {count} samples ({pct:.2f}%)")
    
    # Ensure balanced dataset or at least have both classes
    if len(unique_labels) < 2:
        print("[ERROR] Dataset must have both benign and attack samples!")
        sys.exit(1)
    
    # Split data - ensure stratification for balanced split
    print("\n[TRAIN] Splitting data (80/20 train/test with stratification)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42, 
        stratify=y
    )
    
    print(f"[TRAIN] Training set: {X_train.shape[0]} samples")
    print(f"[TRAIN] Test set: {X_test.shape[0]} samples")
    
    # Check for data quality issues
    if X_train.isnull().sum().sum() > 0:
        print("[WARNING] Found NaN in training data - filling with 0...")
        X_train = X_train.fillna(0)
        X_test = X_test.fillna(0)
    
    # Check for infinite values
    if np.isinf(X_train).sum().sum() > 0 or np.isinf(X_test).sum().sum() > 0:
        print("[ERROR] Found infinite values in data!")
        X_train = np.nan_to_num(X_train, posinf=0, neginf=0)
        X_test = np.nan_to_num(X_test, posinf=0, neginf=0)
        print("[FIXED] Replaced infinite values with 0")
    
    # Scale features
    print("\n[SCALE] Scaling features with StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"[SCALE] Training data - Mean: {X_train_scaled.mean():.6f}, Std: {X_train_scaled.std():.6f}")
    
    # Train logistic regression model
    print("\n[TRAIN] Training Logistic Regression model...")
    print("[TRAIN] Configuration: max_iter=1000, random_state=42, n_jobs=-1")
    
    model = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1, solver='lbfgs')
    try:
        model.fit(X_train_scaled, y_train)
        print("[TRAIN] Model training completed successfully!")
    except Exception as e:
        print(f"[ERROR] Model training failed: {e}")
        print("[TRAIN] Attempting with different solver...")
        model = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1, solver='liblinear')
        model.fit(X_train_scaled, y_train)
        print("[TRAIN] Model training completed with alternative solver!")
    
    # Evaluate
    print("\n[EVALUATE] Computing metrics...")
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"\n[RESULTS]")
    print(f"  Training accuracy: {train_score*100:.2f}%")
    print(f"  Testing accuracy: {test_score*100:.2f}%")
    
    # Get predictions for detailed metrics
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Calculate ROC-AUC
    try:
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        print(f"  ROC-AUC Score: {roc_auc:.4f}")
    except:
        print("  ROC-AUC Score: Unable to compute")
    
    # Classification report
    print(f"\n[CLASSIFICATION REPORT]")
    print(classification_report(y_test, y_pred, target_names=['BENIGN', 'ATTACK']))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"[CONFUSION MATRIX]")
    print(f"  True Negatives (TN): {tn}")
    print(f"  False Positives (FP): {fp}")
    print(f"  False Negatives (FN): {fn}")
    print(f"  True Positives (TP): {tp}")
    
    # Calculate additional metrics
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    print(f"  Sensitivity (True Positive Rate): {sensitivity*100:.2f}%")
    print(f"  Specificity (True Negative Rate): {specificity*100:.2f}%")
    
    # Validate predictions on samples
    print(f"\n[VALIDATION] Testing prediction ranges...")
    benign_test = X_test_scaled[y_test == 0][:10]
    attack_test = X_test_scaled[y_test == 1][:10]
    
    benign_preds = model.predict_proba(benign_test)[:, 1]
    attack_preds = model.predict_proba(attack_test)[:, 1]
    
    print(f"\nBenign predictions (should be mostly < 0.5):")
    print(f"  Values: {benign_preds}")
    print(f"  Mean: {benign_preds.mean():.4f}, Std: {benign_preds.std():.4f}")
    print(f"  Correctly predicted: {sum(benign_preds < 0.5)}/10")
    
    print(f"\nAttack predictions (should be mostly > 0.5):")
    print(f"  Values: {attack_preds}")
    print(f"  Mean: {attack_preds.mean():.4f}, Std: {attack_preds.std():.4f}")
    print(f"  Correctly predicted: {sum(attack_preds > 0.5)}/10")
    
    # Check model parameters
    print(f"\n[MODEL INFO]")
    print(f"  Number of features: {model.n_features_in_}")
    print(f"  Coefficients shape: {model.coef_.shape}")
    print(f"  Intercept: {model.intercept_[0]:.6f}")
    print(f"  Classes: {model.classes_}")
    
    # Save the new model
    print(f"\n[SAVE] Saving new model and scaler...")
    try:
        joblib.dump(model, 'ids_model_logistic.pkl')
        joblib.dump(scaler, 'ids_scaler_logistic.pkl')
        print("[SUCCESS] Model saved successfully!")
        print("  ✓ ids_model_logistic.pkl")
        print("  ✓ ids_scaler_logistic.pkl")
    except Exception as e:
        print(f"[ERROR] Failed to save model: {e}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print(" TRAINING COMPLETED SUCCESSFULLY ".center(70, "="))
    print("="*70)
    
except Exception as e:
    print(f"\n[FATAL ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
