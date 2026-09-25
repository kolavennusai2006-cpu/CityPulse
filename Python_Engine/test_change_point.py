from generator import generate_historical_data

from change_point import analyze_change_point


# ==========================================
# GENERATE HISTORICAL DATA
# ==========================================

historical_data = generate_historical_data(
    num_snapshots=12,
    interval_minutes=5,
    disruption_start=5
)


# ==========================================
# GET ZONE A HISTORY
# ==========================================

zone_index = 0

zone_history = [
    snapshot[zone_index]
    for snapshot in historical_data
]


# ==========================================
# CHANGE-POINT ANALYSIS
# ==========================================

result = analyze_change_point(
    zone_history,
    threshold=10,
    minimum_signals=2
)


# ==========================================
# DISPLAY RESULT
# ==========================================

print("\nCITYPULSE — CHANGE POINT TEST")
print("=" * 50)

print("\nCHANGE DETECTED:")
print(result["change_detected"])

print("\nPRIMARY CHANGE POINT:")
print(result["change_point"])

print("\nALL CHANGE POINTS:")
print(result["all_change_points"])