from statistics import mean, stdev


# ============================================================
# EXISTING SNAPSHOT FEATURE ENGINE
# ============================================================

def create_features(current, baseline, signal_changes):
    """
    Create features for a single civic snapshot.
    """

    features = {
        # Zone information
        "zone_id": current["zone_id"],

        # Raw civic values
        "rainfall_mm": current["weather"]["rainfall_mm"],
        "traffic_percent": current["traffic"]["congestion_percent"],
        "transit_delay_minutes": current["transit"]["delay_minutes"],
        "complaints_count": current["complaints"]["count"],

        # Percentage changes
        "rainfall_change": signal_changes["rainfall_change"],
        "traffic_change": signal_changes["traffic_change"],
        "transit_change": signal_changes["transit_change"],
        "complaints_change": signal_changes["complaints_change"],

        # Cross-signal information
        "signals_detected_count": len(
            signal_changes["signals_detected"]
        ),

        "signal_convergence": (
            1
            if len(signal_changes["signals_detected"]) >= 2
            else 0
        )
    }

    return features


# ============================================================
# TEMPORAL FEATURE HELPERS
# ============================================================

def calculate_rate_of_change(current_value, previous_value):
    """
    Calculate percentage rate of change between
    two consecutive observations.
    """

    if previous_value == 0:

        if current_value > 0:
            return 100

        return 0

    return round(
        ((current_value - previous_value) / previous_value) * 100
    )


def calculate_rolling_statistics(values, window=3):
    """
    Calculate rolling mean and standard deviation.

    Uses the most recent values available.
    """

    if not values:
        return 0, 0

    recent_values = values[-window:]

    rolling_mean = mean(recent_values)

    if len(recent_values) >= 2:
        rolling_std = stdev(recent_values)
    else:
        rolling_std = 0

    return (
        round(rolling_mean, 2),
        round(rolling_std, 2)
    )


def calculate_persistence(values, threshold):
    """
    Measure how many consecutive recent observations
    remain above a threshold.
    """

    persistence = 0

    for value in reversed(values):

        if value >= threshold:
            persistence += 1

        else:
            break

    return persistence


# ============================================================
# HISTORICAL FEATURE ENGINE
# ============================================================

def create_temporal_features(
    zone_history,
    current_index,
    window=3
):
    """
    Create temporal features for one zone.

    zone_history:
        Historical observations for one zone.

    current_index:
        Index of the current observation.

    window:
        Number of recent observations used for rolling statistics.
    """

    current = zone_history[current_index]

    # --------------------------------------------------------
    # Extract signal histories
    # --------------------------------------------------------

    rainfall_history = [
        item["weather"]["rainfall_mm"]
        for item in zone_history[:current_index + 1]
    ]

    traffic_history = [
        item["traffic"]["congestion_percent"]
        for item in zone_history[:current_index + 1]
    ]

    transit_history = [
        item["transit"]["delay_minutes"]
        for item in zone_history[:current_index + 1]
    ]

    complaints_history = [
        item["complaints"]["count"]
        for item in zone_history[:current_index + 1]
    ]

    # --------------------------------------------------------
    # Current values
    # --------------------------------------------------------

    rainfall = current["weather"]["rainfall_mm"]
    traffic = current["traffic"]["congestion_percent"]
    transit = current["transit"]["delay_minutes"]
    complaints = current["complaints"]["count"]

    # --------------------------------------------------------
    # Rate of change
    # --------------------------------------------------------

    if current_index > 0:

        previous = zone_history[current_index - 1]

        rainfall_rate = calculate_rate_of_change(
            rainfall,
            previous["weather"]["rainfall_mm"]
        )

        traffic_rate = calculate_rate_of_change(
            traffic,
            previous["traffic"]["congestion_percent"]
        )

        transit_rate = calculate_rate_of_change(
            transit,
            previous["transit"]["delay_minutes"]
        )

        complaints_rate = calculate_rate_of_change(
            complaints,
            previous["complaints"]["count"]
        )

    else:

        rainfall_rate = 0
        traffic_rate = 0
        transit_rate = 0
        complaints_rate = 0

    # --------------------------------------------------------
    # Rolling statistics
    # --------------------------------------------------------

    rainfall_mean, rainfall_std = calculate_rolling_statistics(
        rainfall_history,
        window
    )

    traffic_mean, traffic_std = calculate_rolling_statistics(
        traffic_history,
        window
    )

    transit_mean, transit_std = calculate_rolling_statistics(
        transit_history,
        window
    )

    complaints_mean, complaints_std = calculate_rolling_statistics(
        complaints_history,
        window
    )

    # --------------------------------------------------------
    # Persistence
    # --------------------------------------------------------

    rainfall_persistence = calculate_persistence(
        rainfall_history,
        threshold=5
    )

    traffic_persistence = calculate_persistence(
        traffic_history,
        threshold=50
    )

    transit_persistence = calculate_persistence(
        transit_history,
        threshold=10
    )

    complaints_persistence = calculate_persistence(
        complaints_history,
        threshold=15
    )

    # --------------------------------------------------------
    # Temporal feature record
    # --------------------------------------------------------

    return {

        "zone_id": current["zone_id"],

        "snapshot_index": current["snapshot_index"],

        "time_offset_minutes": current[
            "time_offset_minutes"
        ],

        # Current values
        "rainfall_mm": rainfall,
        "traffic_percent": traffic,
        "transit_delay_minutes": transit,
        "complaints_count": complaints,

        # Rate of change
        "rainfall_rate": rainfall_rate,
        "traffic_rate": traffic_rate,
        "transit_rate": transit_rate,
        "complaints_rate": complaints_rate,

        # Rolling mean
        "rainfall_rolling_mean": rainfall_mean,
        "traffic_rolling_mean": traffic_mean,
        "transit_rolling_mean": transit_mean,
        "complaints_rolling_mean": complaints_mean,

        # Rolling standard deviation
        "rainfall_rolling_std": rainfall_std,
        "traffic_rolling_std": traffic_std,
        "transit_rolling_std": transit_std,
        "complaints_rolling_std": complaints_std,

        # Persistence
        "rainfall_persistence": rainfall_persistence,
        "traffic_persistence": traffic_persistence,
        "transit_persistence": transit_persistence,
        "complaints_persistence": complaints_persistence
    }


# ============================================================
# HISTORICAL ML FEATURE ENGINE
# ============================================================

def create_historical_ml_features(historical_data):
    """
    Create ML feature records from historical civic data.
    Uses the first observation of each zone as its baseline.
    """

    from detection import detect_signal_changes

    feature_records = []

    # Group historical observations by zone
    zone_histories = {}

    for snapshot in historical_data:

        for zone_data in snapshot:

            zone_id = zone_data["zone_id"]

            if zone_id not in zone_histories:
                zone_histories[zone_id] = []

            zone_histories[zone_id].append(zone_data)

    # Create ML features for every historical observation
    for zone_id, history in zone_histories.items():

        baseline = history[0]

        for current in history:

            signal_changes = detect_signal_changes(
                current,
                baseline
            )

            features = create_features(
                current,
                baseline,
                signal_changes
            )

            feature_records.append(features)

    return feature_records


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from generator import generate_historical_data

    print("CITYPULSE TEMPORAL FEATURE TEST")
    print("=" * 60)

    historical_data = generate_historical_data()

    # --------------------------------------------------------
    # Extract Zone A history
    # --------------------------------------------------------

    zone_a_history = [
        snapshot[0]
        for snapshot in historical_data
    ]

    # --------------------------------------------------------
    # Test the final snapshot
    # --------------------------------------------------------

    current_index = len(zone_a_history) - 1

    features = create_temporal_features(
        zone_a_history,
        current_index
    )

    print("\nZONE:", features["zone_id"])

    print(
        "TIME:",
        f"+{features['time_offset_minutes']} minutes"
    )

    print("\nCURRENT VALUES")

    print(
        "Rainfall:",
        features["rainfall_mm"]
    )

    print(
        "Traffic:",
        features["traffic_percent"]
    )

    print(
        "Transit Delay:",
        features["transit_delay_minutes"]
    )

    print(
        "Complaints:",
        features["complaints_count"]
    )

    print("\nRATE OF CHANGE")

    print(
        "Rainfall:",
        features["rainfall_rate"], "%"
    )

    print(
        "Traffic:",
        features["traffic_rate"], "%"
    )

    print(
        "Transit:",
        features["transit_rate"], "%"
    )

    print(
        "Complaints:",
        features["complaints_rate"], "%"
    )

    print("\nROLLING MEAN")

    print(
        "Rainfall:",
        features["rainfall_rolling_mean"]
    )

    print(
        "Traffic:",
        features["traffic_rolling_mean"]
    )

    print(
        "Transit:",
        features["transit_rolling_mean"]
    )

    print(
        "Complaints:",
        features["complaints_rolling_mean"]
    )

    print("\nROLLING STANDARD DEVIATION")

    print(
        "Rainfall:",
        features["rainfall_rolling_std"]
    )

    print(
        "Traffic:",
        features["traffic_rolling_std"]
    )

    print(
        "Transit:",
        features["transit_rolling_std"]
    )

    print(
        "Complaints:",
        features["complaints_rolling_std"]
    )

    print("\nPERSISTENCE")

    print(
        "Rainfall:",
        features["rainfall_persistence"]
    )

    print(
        "Traffic:",
        features["traffic_persistence"]
    )

    print(
        "Transit:",
        features["transit_persistence"]
    )

    print(
        "Complaints:",
        features["complaints_persistence"]
    )