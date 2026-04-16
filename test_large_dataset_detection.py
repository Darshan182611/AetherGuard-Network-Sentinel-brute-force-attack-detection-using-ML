import requests
import json
import time

print("="*70)
print(" VALIDATING LARGER DATASET DETECTION ".center(70, "="))
print("="*70)

base_url = "http://localhost:5000"

try:
    # Test stream endpoint
    print("\n[TEST] Starting live stream with new 24K sample detection...")
    stream_url = f"{base_url}/stream"
    
    stats = {
        "total_packets": 0,
        "alerts": 0,
        "normal": 0,
        "mismatches": 0,
        "predictions": []
    }
    
    response = requests.get(stream_url, stream=True, timeout=30)
    
    for line in response.iter_lines():
        if not line:
            continue
        
        try:
            # Parse JSON from SSE stream
            if line.startswith(b'data: '):
                json_str = line[6:].decode('utf-8')
                packet = json.loads(json_str)
                
                stats["total_packets"] += 1
                
                if packet.get("status") == "ALERT":
                    stats["alerts"] += 1
                elif packet.get("status") == "NORMAL":
                    stats["normal"] += 1
                
                if packet.get("validation") == "MISMATCH":
                    stats["mismatches"] += 1
                
                # Store some sample predictions
                if len(stats["predictions"]) < 10:
                    stats["predictions"].append({
                        "id": packet.get("packet_id"),
                        "status": packet.get("status"),
                        "confidence": packet.get("confidence"),
                        "actual": packet.get("actual_label")
                    })
                
                # Print progress every 100 packets
                if stats["total_packets"] % 100 == 0:
                    print(f"  Progress: {stats['total_packets']} packets processed...")
                
                # Stop after 24K packets (matching the new sample size)
                if stats["total_packets"] >= 24000:
                    print(f"\n  ✓ Reached 24,000 samples - stopping stream")
                    response.close()
                    break
        except Exception as e:
            continue
    
    # Print results
    print("\n" + "="*70)
    print(" DETECTION RESULTS ".center(70, "="))
    print("="*70)
    
    print(f"\nTotal packets analyzed: {stats['total_packets']}")
    print(f"Attacks detected: {stats['alerts']} ({stats['alerts']/stats['total_packets']*100:.1f}%)")
    print(f"Normal traffic: {stats['normal']} ({stats['normal']/stats['total_packets']*100:.1f}%)")
    print(f"Mismatches: {stats['mismatches']} ({stats['mismatches']/stats['total_packets']*100:.2f}%)")
    
    print(f"\n[SAMPLE PREDICTIONS]")
    print(f"  {'ID':<5} {'Predicted':<10} {'Confidence':<12} {'Actual':<10}")
    print(f"  {'-'*5} {'-'*10} {'-'*12} {'-'*10}")
    for pred in stats["predictions"]:
        print(f"  {pred['id']:<5} {pred['status']:<10} {pred['confidence']:<12} {pred['actual']:<10}")
    
    print("\n" + "="*70)
    
    # Verify results
    if stats["total_packets"] > 200:
        print(f"\n✓ VERIFIED: Using {stats['total_packets']} samples (NOT just 200!)")
        print(f"✓ Detection rate: {stats['alerts']/stats['total_packets']*100:.1f}% attacks detected")
    else:
        print(f"\n✗ BUG STILL EXISTS: Only {stats['total_packets']} samples used")
    
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
