# ==========================================
# CITYPULSE — CHANGE POINT DETECTION
# ==========================================


SIGNALS = [
    "rainfall_mm",
    "traffic_percent",
    "transit_delay_minutes",
    "complaints_count"
]


def calculate_signal_change(previous, current):
    """
    Calculate percentage change between
    two consecutive CityPulse observations.
    """

    previous_values = {
        "rainfall_mm": previous["weather"]["rainfall_mm"],
        "traffic_percent": previous["traffic"]["congestion_percent"],
        "transit_delay_minutes": previous["transit"]["delay_minutes"],
        "complaints_count": previous["complaints"]["count"]
    }

    current_values = {
        "rainfall_mm": current["weather"]["rainfall_mm"],
        "traffic_percent": current["traffic"]["congestion_percent"],
        "transit_delay_minutes": current["transit"]["delay_minutes"],
        "complaints_count": current["complaints"]["count"]
    }

    changes = {}

    for signal in SIGNALS:

        previous_value = previous_values[signal]
        current_value = current_values[signal]

        if previous_value == 0:

            if current_value > 0:
                changes[signal] = 100
            else:
                changes[signal] = 0

        else:

            change = (
                (current_value - previous_value)
                / previous_value
            ) * 100

            changes[signal] = round(change, 2)

    return changes


def detect_change_points(
    zone_history,
    threshold=10,
    minimum_signals=2
):
    """
    Detect the first point where multiple
    civic signals change simultaneously.

    threshold:
        Minimum percentage increase required.

    minimum_signals:
        Minimum number of signals that must
        cross the threshold.
    """

    change_points = []

    for index in range(1, len(zone_history)):

        previous = zone_history[index - 1]

        current = zone_history[index]

        changes = calculate_signal_change(
            previous,
            current
        )

        signals_changed = [
            signal
            for signal, change in changes.items()
            if change >= threshold
        ]

        if len(signals_changed) >= minimum_signals:

            change_points.append({

                "snapshot_index": index,

                "time_offset_minutes": (
                    current.get(
                        "time_offset_minutes",
                        index * 5
                    )
                ),

                "signals_changed": signals_changed,

                "changes": changes,

                "signals_changed_count": len(
                    signals_changed
                )
            })

    return change_points


def get_primary_change_point(
    change_points
):
    """
    Return the first detected change point.
    """

    if not change_points:

        return {
            "change_detected": False,
            "change_point": None
        }

    return {
        "change_detected": True,
        "change_point": change_points[0]
    }


def analyze_change_point(
    zone_history,
    threshold=10,
    minimum_signals=2
):
    """
    Complete change-point analysis.
    """

    change_points = detect_change_points(
        zone_history,
        threshold=threshold,
        minimum_signals=minimum_signals
    )

    primary_change = get_primary_change_point(
        change_points
    )

    return {
        "change_detected": primary_change[
            "change_detected"
        ],

        "change_point": primary_change[
            "change_point"
        ],

        "all_change_points": change_points
    }