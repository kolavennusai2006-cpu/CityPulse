def build_intelligence_output(
    zone_id,
    detection_result,
    temporal_result,
    event_result,
    ml_result,
    statistical_result,
    ensemble_result,
    change_point_result,
    early_warning_result,
    recovery_result,
    lifecycle_result
):
    return {
        "zone_id": zone_id,

        "status": detection_result["status"],

        "risk_score": detection_result["risk_score"],

        "anomaly": detection_result["anomaly"],

        "signals_detected": detection_result["signals_detected"],

        "why_flagged": detection_result["why_flagged"],

        "ml": ml_result,

        "statistical": statistical_result,

        "ensemble": ensemble_result,

        "early_warning": early_warning_result,

        "change_point": change_point_result,

        "temporal": {
            "state": temporal_result["temporal_state"],
            "persistence_score": temporal_result["persistence_score"],
            "acceleration_score": temporal_result["acceleration_score"],
            "convergence_score": temporal_result["convergence_score"]
        },

        "event": event_result,

        "recovery": recovery_result,

        "event_lifecycle": lifecycle_result
    }