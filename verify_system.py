import os
import joblib
import sys

print("="*70)
print(" FINAL SYSTEM VERIFICATION ".center(70, "="))
print("="*70)

all_checks = []

# Check 1: Model files exist
print("\n[CHECK 1] Model files existence...")
model_files = {
    'ids_model_logistic.pkl': os.path.exists('ids_model_logistic.pkl'),
    'ids_scaler_logistic.pkl': os.path.exists('ids_scaler_logistic.pkl'),
}

for file, exists in model_files.items():
    status = "✓" if exists else "✗"
    print(f"  {status} {file}")
    all_checks.append(exists)

# Check 2: Model file sizes
print("\n[CHECK 2] Model file sizes...")
if os.path.exists('ids_model_logistic.pkl'):
    size_kb = os.path.getsize('ids_model_logistic.pkl') / 1024
    print(f"  ✓ Model: {size_kb:.2f} KB")
    all_checks.append(True)
else:
    print(f"  ✗ Model file not found")
    all_checks.append(False)

if os.path.exists('ids_scaler_logistic.pkl'):
    size_kb = os.path.getsize('ids_scaler_logistic.pkl') / 1024
    print(f"  ✓ Scaler: {size_kb:.2f} KB")
    all_checks.append(True)
else:
    print(f"  ✗ Scaler file not found")
    all_checks.append(False)

# Check 3: Load and verify model
print("\n[CHECK 3] Loading and verifying model...")
try:
    model = joblib.load('ids_model_logistic.pkl')
    scaler = joblib.load('ids_scaler_logistic.pkl')
    print(f"  ✓ Model loaded successfully")
    print(f"    - Type: {type(model).__name__}")
    print(f"    - Features: {model.n_features_in_}")
    print(f"    - Classes: {list(model.classes_)}")
    all_checks.append(True)
except Exception as e:
    print(f"  ✗ Failed to load model: {e}")
    all_checks.append(False)
    sys.exit(1)

# Check 4: Python version and dependencies
print("\n[CHECK 4] Python environment...")
print(f"  ✓ Python {sys.version.split()[0]}")
print(f"  ✓ joblib version: {joblib.__version__}")

try:
    import pandas as pd
    print(f"  ✓ pandas available")
    all_checks.append(True)
except:
    print(f"  ✗ pandas not available")
    all_checks.append(False)

try:
    import sklearn
    print(f"  ✓ scikit-learn available")
    all_checks.append(True)
except:
    print(f"  ✗ scikit-learn not available")
    all_checks.append(False)

# Check 5: Application files
print("\n[CHECK 5] Application files...")
app_files = {
    'app.py': os.path.exists('app.py'),
    'live_ids_monitor.py': os.path.exists('live_ids_monitor.py'),
    'train_working_model.py': os.path.exists('train_working_model.py'),
}

for file, exists in app_files.items():
    status = "✓" if exists else "✗"
    print(f"  {status} {file}")
    all_checks.append(exists)

# Final summary
print("\n" + "="*70)
checks_passed = sum(all_checks)
total_checks = len(all_checks)
print(f" VERIFICATION RESULTS: {checks_passed}/{total_checks} PASSED ".center(70, "="))
print("="*70)

if all(all_checks):
    print("\n✓ ALL CHECKS PASSED - SYSTEM READY FOR DEPLOYMENT\n")
    sys.exit(0)
else:
    print("\n✗ SOME CHECKS FAILED - PLEASE FIX ISSUES\n")
    sys.exit(1)
