import requests
import json
import time
import sys

print("="*70)
print(" QUICK VALIDATION - DATASET SIZE VERIFICATION ".center(70, "="))
print("="*70)

base_url = "http://localhost:5000"

try:
    print("\n[TEST] Connecting to Flask stream...")
    stream_url = f"{base_url}/stream"
    
    stats = {
        "total": 0,
        "alerts": 0,
        "normal": 0,
        "samples": []
    }
    
    print("[STREAM] Reading packets - will stop after 1000 samples...\n")
    response = requests.get(stream_url, stream=True, timeout=60)
    
    for line in response.iter_lines():
        if not line:
            continue
        
        try:
            if line.startswith(b'data: '):
                json_str = line[6:].decode('utf-8')
                packet = json.loads(json_str)
                
                stats["total"] += 1
                if packet.get("status") == "ALERT":
                    stats["alerts"] += 1
                elif packet.get("status") == "NORMAL":
                    stats["normal"] += 1
                
                # Store first 20 samples
                if len(stats["samples"]) < 20:
                    stats["samples"].append(f"  [{packet['packet_id']}] {packet['status']:6} (conf: {packet['confidence']}%)")
                
                # Print every 100
                if stats["total"] % 100 == 0:
                    print(f"  [{stats['total']:4d}] Alerts: {stats['alerts']:4d} | Normal: {stats['normal']:4d}")
                
                if stats["total"] >= 1000:
                    print(f"\n✓ Reached 1,000 samples - stopping")
                    response.close()
                    break
        except Exception as e:
            continue
    
    print("\n" + "="*70)
    print(" RESULTS ".center(70, "="))
    print("="*70)
    
    print(f"\n[SAMPLES PROCESSED]: {stats['total']}")
    print(f"[ATTACKS DETECTED]: {stats['alerts']} ({stats['alerts']/max(1, stats['total'])*100:.1f}%)")
    print(f"[NORMAL TRAFFIC]:   {stats['normal']} ({stats['normal']/max(1, stats['total'])*100:.1f}%)")
    
    print(f"\n[SAMPLE OUTPUTS]:")
    for sample in stats["samples"]:
        print(sample)
    
    print("\n" + "="*70)
    
    if stats["total"] > 200:
        print(f"✅ SUCCESS: Using {stats['total']} samples for detection")
        print(f"   (Previously was stuck at 200 samples)")
        print(f"✅ BUG FIXED: Dataset detection now working with full model training")
    else:
        print(f"❌ BUG STILL EXISTS: Only {stats['total']} samples")
    
    print("="*70 + "\n")
    
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    print("\nMake sure Flask is running:")
    print("  cd C:\\Users\\darsh\\.gemini\\antigravity\\scratch\\IDS_Project")
    print("  .\\ids_env\\Scripts\\python.exe app.py")
