from generator import generate_historical_data
from recovery_engine import detect_recovery


historical_data = generate_historical_data(
    num_snapshots=12,
    interval_minutes=5,
    disruption_start=5
)

zone_history = [
    snapshot[0]
    for snapshot in historical_data
]


result = detect_recovery(
    zone_history,
    recovery_threshold=5,
    minimum_signals=2
)


print("\nCITYPULSE — RECOVERY TEST")
print("=" * 50)

print("\nRECOVERY DETECTED:")
print(result["recovery_detected"])

print("\nRECOVERY LEVEL:")
print(result["recovery_level"])

print("\nSIGNALS RECOVERING:")
print(result["signals_recovering"])

print("\nSIGNAL COUNT:")
print(result["signals_count"])

print("\nREASON:")
print(result["reason"])

print("\nRECOVERY CHANGES:")
print(result["recovery_changes"])