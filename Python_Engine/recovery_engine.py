# ==========================================
# CITYPULSE — RECOVERY ENGINE
# ==========================================

SIGNALS = [
    "rainfall_mm",
    "traffic_percent",
    "transit_delay_minutes",
    "complaints_count"
]


def get_signal_values(snapshot):

    return {
        "rainfall_mm": snapshot["weather"]["rainfall_mm"],
        "traffic_percent": snapshot["traffic"]["congestion_percent"],
        "transit_delay_minutes": snapshot["transit"]["delay_minutes"],
        "complaints_count": snapshot["complaints"]["count"]
    }


def calculate_recovery(previous, current):

    previous_values = get_signal_values(previous)
    current_values = get_signal_values(current)

    recovery = {}

    for signal in SIGNALS:

        previous_value = previous_values[signal]
        current_value = current_values[signal]

        # If current value is lower,
        # the signal is recovering.
        if current_value < previous_value:

            recovery_percent = (
                (previous_value - current_value)
                / previous_value
            ) * 100

        else:

            recovery_percent = 0

        recovery[signal] = round(
            recovery_percent,
            2
        )

    return recovery


def detect_recovery(
    zone_history,
    recovery_threshold=5,
    minimum_signals=2
):

    if len(zone_history) < 2:

        return {
            "recovery_detected": False,
            "signals_recovering": [],
            "signals_count": 0,
            "recovery_level": "NONE",
            "reason": "Insufficient historical data.",
            "recovery_changes": {}
        }

    previous = zone_history[-2]
    current = zone_history[-1]

    recovery = calculate_recovery(
        previous,
        current
    )

    signals_recovering = [
        signal
        for signal, decrease in recovery.items()
        if decrease >= recovery_threshold
    ]

    signal_count = len(
        signals_recovering
    )

    if signal_count >= minimum_signals:

        if signal_count >= 3:
            recovery_level = "HIGH"
        else:
            recovery_level = "MEDIUM"

        return {
            "recovery_detected": True,
            "signals_recovering": signals_recovering,
            "signals_count": signal_count,
            "recovery_level": recovery_level,
            "reason":
                "Multiple civic signals are "
                "showing signs of recovery.",
            "recovery_changes": recovery
        }

    return {
        "recovery_detected": False,
        "signals_recovering": signals_recovering,
        "signals_count": signal_count,
        "recovery_level": "NONE",
        "reason":
            "No sufficient multi-signal "
            "recovery detected.",
        "recovery_changes": recovery
    }