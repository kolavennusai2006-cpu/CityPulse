import math


def calculate_z_score(current, values):
    """
    Calculate how far the current value is from
    the historical mean in terms of standard deviation.
    """

    if len(values) < 2:
        return 0

    mean = sum(values) / len(values)

    variance = sum(
        (value - mean) ** 2
        for value in values
    ) / len(values)

    standard_deviation = math.sqrt(variance)

    if standard_deviation == 0:
        return 0

    return round(
        (current - mean) / standard_deviation,
        2
    )


def detect_statistical_anomaly(
    current_value,
    historical_values,
    threshold=2
):
    """
    Detect whether the current value is statistically unusual.

    threshold=2 means the current value is approximately
    2 standard deviations away from the historical mean.
    """

    z_score = calculate_z_score(
        current_value,
        historical_values
    )

    anomaly = abs(z_score) >= threshold

    return {
        "z_score": z_score,
        "statistical_anomaly": bool(anomaly)
    }


def analyze_signal_statistics(
    current,
    historical_values
):
    """
    Analyze all four CityPulse civic signals.
    """

    rainfall_result = detect_statistical_anomaly(
        current["weather"]["rainfall_mm"],
        historical_values["rainfall"]
    )

    traffic_result = detect_statistical_anomaly(
        current["traffic"]["congestion_percent"],
        historical_values["traffic"]
    )

    transit_result = detect_statistical_anomaly(
        current["transit"]["delay_minutes"],
        historical_values["transit"]
    )

    complaints_result = detect_statistical_anomaly(
        current["complaints"]["count"],
        historical_values["complaints"]
    )

    return {
        "rainfall": rainfall_result,
        "traffic": traffic_result,
        "transit": transit_result,
        "complaints": complaints_result
    }