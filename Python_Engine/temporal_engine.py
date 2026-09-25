# ============================================================
# CITYPULSE TEMPORAL ENGINE
# ============================================================


def calculate_persistence_score(temporal_features):
    """
    Determine whether abnormal conditions are persisting.
    """

    persistence_values = [
        temporal_features["rainfall_persistence"],
        temporal_features["traffic_persistence"],
        temporal_features["transit_persistence"],
        temporal_features["complaints_persistence"]
    ]

    persistent_signals = sum(
        value >= 3
        for value in persistence_values
    )

    return persistent_signals


def calculate_acceleration_score(temporal_features):
    """
    Determine whether multiple civic signals
    are continuing to increase.
    """

    rate_values = [
        temporal_features["rainfall_rate"],
        temporal_features["traffic_rate"],
        temporal_features["transit_rate"],
        temporal_features["complaints_rate"]
    ]

    increasing_signals = sum(
        value > 0
        for value in rate_values
    )

    return increasing_signals


def calculate_convergence_score(temporal_features):
    """
    Measure how many civic signals are simultaneously
    showing persistent abnormal behavior.
    """

    persistence_values = [
        temporal_features["rainfall_persistence"],
        temporal_features["traffic_persistence"],
        temporal_features["transit_persistence"],
        temporal_features["complaints_persistence"]
    ]

    converging_signals = sum(
        value >= 3
        for value in persistence_values
    )

    return converging_signals


def determine_temporal_state(
    persistence_score,
    acceleration_score,
    convergence_score
):
    """
    Determine the temporal state of a civic zone.
    """

    if (
        convergence_score >= 3
        and acceleration_score >= 3
        and persistence_score >= 3
    ):
        return "DEVELOPING"

    if (
        convergence_score >= 2
        and persistence_score >= 2
    ):
        return "PERSISTENT"

    if acceleration_score >= 2:
        return "ACCELERATING"

    return "STABLE"


def analyze_temporal_state(temporal_features):
    """
    Analyze the temporal behavior of one civic zone.
    """

    persistence_score = calculate_persistence_score(
        temporal_features
    )

    acceleration_score = calculate_acceleration_score(
        temporal_features
    )

    convergence_score = calculate_convergence_score(
        temporal_features
    )

    temporal_state = determine_temporal_state(
        persistence_score,
        acceleration_score,
        convergence_score
    )

    return {
        "zone_id": temporal_features["zone_id"],

        "snapshot_index": temporal_features[
            "snapshot_index"
        ],

        "time_offset_minutes": temporal_features[
            "time_offset_minutes"
        ],

        "persistence_score": persistence_score,

        "acceleration_score": acceleration_score,

        "convergence_score": convergence_score,

        "temporal_state": temporal_state
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from generator import generate_historical_data
    from features import create_temporal_features

    print("CITYPULSE TEMPORAL ENGINE TEST")
    print("=" * 60)

    historical_data = generate_historical_data()

    # --------------------------------------------------------
    # Test Zone A
    # --------------------------------------------------------

    zone_a_history = [
        snapshot[0]
        for snapshot in historical_data
    ]

    current_index = len(zone_a_history) - 1

    temporal_features = create_temporal_features(
        zone_a_history,
        current_index
    )

    result = analyze_temporal_state(
        temporal_features
    )

    print("\nZONE:", result["zone_id"])

    print(
        "TIME:",
        f"+{result['time_offset_minutes']} minutes"
    )

    print(
        "PERSISTENCE SCORE:",
        result["persistence_score"]
    )

    print(
        "ACCELERATION SCORE:",
        result["acceleration_score"]
    )

    print(
        "CONVERGENCE SCORE:",
        result["convergence_score"]
    )

    print(
        "TEMPORAL STATE:",
        result["temporal_state"]
    )