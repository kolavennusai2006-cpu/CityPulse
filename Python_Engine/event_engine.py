# ============================================================
# CITYPULSE EVENT ENGINE
# ============================================================


def detect_event_start(zone_history):
    """
    Find the first snapshot where multiple civic signals
    begin showing a significant increase.
    """

    for index, snapshot in enumerate(zone_history):

        if index == 0:
            continue

        previous = zone_history[index - 1]

        changed_signals = 0

        # Rainfall
        if (
            snapshot["weather"]["rainfall_mm"]
            > previous["weather"]["rainfall_mm"]
        ):
            changed_signals += 1

        # Traffic
        if (
            snapshot["traffic"]["congestion_percent"]
            > previous["traffic"]["congestion_percent"]
        ):
            changed_signals += 1

        # Transit
        if (
            snapshot["transit"]["delay_minutes"]
            > previous["transit"]["delay_minutes"]
        ):
            changed_signals += 1

        # Complaints
        if (
            snapshot["complaints"]["count"]
            > previous["complaints"]["count"]
        ):
            changed_signals += 1

        # Event begins when at least two signals
        # start increasing together.
        if changed_signals >= 2:

            return {
                "snapshot_index": snapshot["snapshot_index"],
                "time_offset_minutes": snapshot[
                    "time_offset_minutes"
                ]
            }

    return None


def extract_signal_evidence(snapshot):
    """
    Extract the civic signal values supporting an event.
    """

    return {
        "rainfall_mm": snapshot["weather"]["rainfall_mm"],
        "traffic_percent": snapshot["traffic"]["congestion_percent"],
        "transit_delay_minutes": snapshot["transit"]["delay_minutes"],
        "complaints_count": snapshot["complaints"]["count"]
    }


def build_event_timeline(zone_history):
    """
    Create a timeline showing how the civic situation evolved.
    """

    timeline = []

    for snapshot in zone_history:

        timeline.append({
            "snapshot_index": snapshot["snapshot_index"],
            "time_offset_minutes": snapshot[
                "time_offset_minutes"
            ],
            "evidence": extract_signal_evidence(
                snapshot
            )
        })

    return timeline


def reconstruct_event(
    zone_history,
    temporal_analysis
):
    """
    Reconstruct a structured civic event from
    historical data and temporal analysis.
    """

    event_start = detect_event_start(
        zone_history
    )

    timeline = build_event_timeline(
        zone_history
    )

    if event_start is None:

        return {
            "event_detected": False,
            "zone_id": zone_history[0]["zone_id"],
            "event_start": None,
            "temporal_state": temporal_analysis[
                "temporal_state"
            ],
            "timeline": timeline,
            "evidence": []
        }

    start_index = event_start["snapshot_index"]

    start_snapshot = zone_history[start_index]

    return {
        "event_detected": True,

        "zone_id": zone_history[0]["zone_id"],

        "event_start": event_start,

        "event_end": {
            "snapshot_index": zone_history[-1][
                "snapshot_index"
            ],
            "time_offset_minutes": zone_history[-1][
                "time_offset_minutes"
            ]
        },

        "duration_minutes": (
            zone_history[-1]["time_offset_minutes"]
            - event_start["time_offset_minutes"]
        ),

        "temporal_state": temporal_analysis[
            "temporal_state"
        ],

        "timeline": timeline,

        "evidence": extract_signal_evidence(
            start_snapshot
        )
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from generator import generate_historical_data
    from features import create_temporal_features
    from temporal_engine import analyze_temporal_state

    print("CITYPULSE EVENT ENGINE TEST")
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
    # Create temporal analysis
    # --------------------------------------------------------

    current_index = len(zone_a_history) - 1

    temporal_features = create_temporal_features(
        zone_a_history,
        current_index
    )

    temporal_analysis = analyze_temporal_state(
        temporal_features
    )

    # --------------------------------------------------------
    # Reconstruct event
    # --------------------------------------------------------

    event = reconstruct_event(
        zone_a_history,
        temporal_analysis
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\nZONE:", event["zone_id"])

    print(
        "EVENT DETECTED:",
        event["event_detected"]
    )

    print(
        "TEMPORAL STATE:",
        event["temporal_state"]
    )

    print(
        "EVENT START:",
        event["event_start"]
    )

    print(
        "EVENT END:",
        event["event_end"]
    )

    print(
        "DURATION:",
        event["duration_minutes"],
        "minutes"
    )

    print("\nEVENT EVIDENCE:")

    for key, value in event["evidence"].items():
        print(f"{key}: {value}")

    print("\nEVENT TIMELINE:")

    for point in event["timeline"]:
        print(
            f"+{point['time_offset_minutes']} min",
            "→",
            point["evidence"]
        )