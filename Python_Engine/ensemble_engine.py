def calculate_ensemble_result(
    rule_anomaly,
    statistical_anomaly,
    ml_anomaly
):
    """
    Combine three independent anomaly detectors.

    Rule-based:
    Detects domain-specific civic threshold violations.

    Statistical:
    Detects unusual deviation from historical behavior.

    ML:
    Detects unusual multi-feature patterns.
    """

    detectors = {
        "rule": bool(rule_anomaly),
        "statistical": bool(statistical_anomaly),
        "ml": bool(ml_anomaly)
    }

    agreement_count = sum(detectors.values())

    if agreement_count >= 2:
        ensemble_anomaly = True
    else:
        ensemble_anomaly = False

    if agreement_count == 3:
        confidence = "HIGH"
    elif agreement_count == 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return {
        "rule_anomaly": detectors["rule"],
        "statistical_anomaly": detectors["statistical"],
        "ml_anomaly": detectors["ml"],
        "detectors_agreeing": agreement_count,
        "ensemble_anomaly": ensemble_anomaly,
        "confidence": confidence
    }