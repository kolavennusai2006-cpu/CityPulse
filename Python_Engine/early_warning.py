# ==========================================
# CITYPULSE — EARLY WARNING ENGINE
# ==========================================


SIGNALS = [
    "rainfall_mm",
    "traffic_percent",
    "transit_delay_minutes",
    "complaints_count"
]


def calculate_signal_trends(zone_history, window=3):
    """
    Calculate recent trends for civic signals.
    """

    if len(zone_history) < window + 1:
        return {}

    recent = zone_history[-(window + 1):]

    trends = {}

    for signal in SIGNALS:

        values = []

        for snapshot in recent:

            if signal == "rainfall_mm":
                value = snapshot["weather"]["rainfall_mm"]

            elif signal == "traffic_percent":
                value = snapshot["traffic"]["congestion_percent"]

            elif signal == "transit_delay_minutes":
                value = snapshot["transit"]["delay_minutes"]

            elif signal == "complaints_count":
                value = snapshot["complaints"]["count"]

            values.append(value)

        changes = []

        for i in range(1, len(values)):

            previous = values[i - 1]
            current = values[i]

            if previous == 0:

                if current > 0:
                    change = 100
                else:
                    change = 0

            else:

                change = (
                    (current - previous)
                    / previous
                ) * 100

            changes.append(round(change, 2))

        trends[signal] = {
            "recent_values": values,
            "recent_changes": changes,
            "average_change": round(
                sum(changes) / len(changes),
                2
            )
        }

    return trends


def detect_early_warning(
    zone_history,
    change_threshold=5,
    minimum_signals=2
):
    """
    Detect whether multiple civic signals
    are showing early deterioration.
    """

    trends = calculate_signal_trends(
        zone_history
    )

    if not trends:

        return {
            "early_warning": False,
            "signals_showing_change": [],
            "warning_level": "NONE",
            "reason": "Insufficient historical data."
        }

    signals_showing_change = []

    for signal, result in trends.items():

        if result["average_change"] >= change_threshold:

            signals_showing_change.append(
                signal
            )

    signal_count = len(
        signals_showing_change
    )

    if signal_count >= minimum_signals:

        if signal_count >= 3:
            warning_level = "HIGH"

        else:
            warning_level = "MEDIUM"

        return {
            "early_warning": True,
            "signals_showing_change":
                signals_showing_change,
            "signals_count": signal_count,
            "warning_level": warning_level,
            "reason":
                "Multiple civic signals are "
                "showing a sustained upward trend.",
            "trends": trends
        }

    return {
        "early_warning": False,
        "signals_showing_change":
            signals_showing_change,
        "signals_count": signal_count,
        "warning_level": "NONE",
        "reason":
            "No sufficient multi-signal "
            "deterioration detected.",
        "trends": trends
    }