import requests
import time
import re

print("="*70)
print(" FLASK APP INTEGRATION TEST ".center(70, "="))
print("="*70)

base_url = "http://localhost:5000"

try:
    # Test 1: Check if server is responding
    print("\n[TEST 1] Checking Flask server availability...")
    response = requests.get(base_url, timeout=5)
    print(f"  ✓ Server responding with status: {response.status_code}")
    
    # Test 2: Test stream endpoint for 2 seconds
    print("\n[TEST 2] Testing live stream endpoint...")
    stream_url = f"{base_url}/stream"
    
    detections = {"ALERT": 0, "NORMAL": 0}
    packets_received = 0
    
    response = requests.get(stream_url, stream=True, timeout=5)
    start_time = time.time()
    
    for line in response.iter_lines():
        if time.time() - start_time > 2:  # Only read for 2 seconds
            break
        
        if line:
            packets_received += 1
            # Look for status in the stream data
            if b'ALERT' in line or 'ALERT' in str(line):
                detections["ALERT"] += 1
            elif b'NORMAL' in line or 'NORMAL' in str(line):
                detections["NORMAL"] += 1
    
    print(f"  ✓ Packets received: {packets_received}")
    print(f"  ✓ Alerts (attacks): {detections['ALERT']}")
    print(f"  ✓ Normal traffic: {detections['NORMAL']}")
    
    # Test 3: Verify we're getting mixed results (not all one type)
    print("\n[TEST 3] Checking for mixed detection results...")
    if detections["ALERT"] > 0 and detections["NORMAL"] > 0:
        print(f"  ✓ Getting mixed detections (not all alerts, not all normal)")
    elif detections["ALERT"] > 0:
        print(f"  ⚠ Warning: Only getting alerts, no normal traffic detected")
    elif detections["NORMAL"] > 0:
        print(f"  ⚠ Warning: Only getting normal traffic, no attacks detected")
    else:
        print(f"  ✗ ERROR: No traffic data detected in stream")
    
    print("\n" + "="*70)
    print(" FLASK INTEGRATION TEST COMPLETED ".center(70, "="))
    print("="*70)
    
except requests.exceptions.ConnectionError:
    print("  ✗ ERROR: Cannot connect to Flask server")
    print("  Make sure Flask is running: python app.py")
except Exception as e:
    print(f"  ✗ ERROR: {e}")
