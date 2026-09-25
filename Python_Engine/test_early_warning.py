from generator import generate_historical_data

from early_warning import detect_early_warning


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
# EARLY WARNING ANALYSIS
# ==========================================

result = detect_early_warning(
    zone_history,
    change_threshold=5,
    minimum_signals=2
)


# ==========================================
# DISPLAY RESULT
# ==========================================

print("\nCITYPULSE — EARLY WARNING TEST")
print("=" * 50)

print("\nEARLY WARNING:")
print(result["early_warning"])

print("\nWARNING LEVEL:")
print(result["warning_level"])

print("\nSIGNALS SHOWING CHANGE:")
print(result["signals_showing_change"])

print("\nREASON:")
print(result["reason"])

print("\nTRENDS:")
print(result["trends"])