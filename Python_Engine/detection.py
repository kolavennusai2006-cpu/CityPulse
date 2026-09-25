def percentage_change(current, baseline):
    """
    Calculate percentage change between current and baseline.
    """

    if baseline == 0:
        if current > 0:
            return 100
        return 0

    return round(((current - baseline) / baseline) * 100)


def detect_signal_changes(current, baseline):
    """
    Detect abnormal changes in the four civic signals.
    """

    rainfall_change = percentage_change(
        current["weather"]["rainfall_mm"],
        baseline["weather"]["rainfall_mm"]
    )

    traffic_change = percentage_change(
        current["traffic"]["congestion_percent"],
        baseline["traffic"]["congestion_percent"]
    )

    transit_change = percentage_change(
        current["transit"]["delay_minutes"],
        baseline["transit"]["delay_minutes"]
    )

    complaints_change = percentage_change(
        current["complaints"]["count"],
        baseline["complaints"]["count"]
    )

    signals_detected = []

    if rainfall_change >= 50:
        signals_detected.append("HEAVY_RAIN")

    if traffic_change >= 30:
        signals_detected.append("TRAFFIC_SPIKE")

    if transit_change >= 30:
        signals_detected.append("TRANSIT_DELAY")

    if complaints_change >= 30:
        signals_detected.append("COMPLAINT_SPIKE")

    return {
        "rainfall_change": rainfall_change,
        "traffic_change": traffic_change,
        "transit_change": transit_change,
        "complaints_change": complaints_change,
        "signals_detected": signals_detected
    }


def calculate_risk_score(signal_changes):
    """
    Calculate risk score from 0 to 100.
    """

    score = 0

    if "HEAVY_RAIN" in signal_changes["signals_detected"]:
        score += 25

    if "TRAFFIC_SPIKE" in signal_changes["signals_detected"]:
        score += 25

    if "TRANSIT_DELAY" in signal_changes["signals_detected"]:
        score += 25

    if "COMPLAINT_SPIKE" in signal_changes["signals_detected"]:
        score += 25

    return score


def get_status(risk_score):
    """
    Convert risk score into CityPulse status.
    """

    if risk_score >= 75:
        return "CRITICAL"

    if risk_score >= 50:
        return "EMERGING"

    if risk_score >= 30:
        return "WATCH"

    return "NORMAL"


def create_why_flagged(signal_changes):
    """
    Create evidence explaining why a zone was flagged.
    """

    evidence = []

    changes = [
        ("Rainfall", signal_changes["rainfall_change"]),
        ("Traffic", signal_changes["traffic_change"]),
        ("Transit Delay", signal_changes["transit_change"]),
        ("Complaints", signal_changes["complaints_change"])
    ]

    for signal, change in changes:

        if change >= 30:
            evidence.append({
                "signal": signal,
                "change_percent": change
            })

    # Normal zone
    if len(signal_changes["signals_detected"]) < 2:

        return {
            "reason": "No significant civic disruption detected.",
            "evidence": [],
            "time_window_minutes": 15,
            "interpretation": "Current signals are within normal range."
        }

    # Anomalous zone
    return {
        "reason": "Multiple civic signals changed significantly within the same time window.",
        "evidence": evidence,
        "time_window_minutes": 15,
        "interpretation": (
            "These signals show a possible relationship. "
            "This does not confirm causation."
        )
    }


def analyze_zone(current, baseline):
    """
    Analyze one zone and return its detection result.
    """

    signal_changes = detect_signal_changes(
        current,
        baseline
    )

    risk_score = calculate_risk_score(
        signal_changes
    )

    status = get_status(
        risk_score
    )

    anomaly = len(
        signal_changes["signals_detected"]
    ) >= 2

    why_flagged = create_why_flagged(
        signal_changes
    )

    return {
        "zone_id": current["zone_id"],
        "status": status,
        "risk_score": risk_score,
        "anomaly": anomaly,
        "signals_detected": signal_changes["signals_detected"],
        "why_flagged": why_flagged
    }


def analyze_city(normal_data, current_data):
    """
    Analyze all five city zones.

    normal_data:
        Stable baseline data.

    current_data:
        Current civic data.

    Returns:
        List containing the analysis result for every zone.
    """

    results = []

    for baseline, current in zip(
        normal_data,
        current_data
    ):

        result = analyze_zone(
            current,
            baseline
        )

        results.append(result)

    return results


# Test the complete detection system
if __name__ == "__main__":

    from generator import generate_city_data

    print("CITYPULSE DETECTION TEST")
    print("=" * 60)

    # Generate stable baseline
    normal_data = generate_city_data(
        disruption=False
    )

    # Generate current scenario
    current_data = generate_city_data(
        disruption=True
    )

    # Analyze complete city
    city_results = analyze_city(
        normal_data,
        current_data
    )

    # Display results
    for result in city_results:

        print("\n" + "=" * 60)

        print("ZONE:", result["zone_id"])
        print("STATUS:", result["status"])
        print("RISK SCORE:", result["risk_score"])
        print("ANOMALY:", result["anomaly"])
        print("SIGNALS:", result["signals_detected"])
        print("WHY FLAGGED:", result["why_flagged"])