import json

from generator import generate_city_data, generate_historical_data
from detection import analyze_city
from features import create_temporal_features, create_historical_ml_features
from ml_engine import train_anomaly_model, predict_anomaly
from statistical_engine import analyze_signal_statistics
from ensemble_engine import calculate_ensemble_result
from temporal_engine import analyze_temporal_state
from event_engine import reconstruct_event
from change_point import analyze_change_point
from early_warning import detect_early_warning
from recovery_engine import detect_recovery
from event_lifecycle import determine_event_lifecycle
from intelligence_output import build_intelligence_output


# ============================================================
# 1. GENERATE CITY DATA
# ============================================================

normal_data = generate_city_data(disruption=False)

current_data = generate_city_data(disruption=True)


# ============================================================
# 2. GENERATE HISTORICAL DATA
# ============================================================

historical_data = generate_historical_data(
    num_snapshots=12,
    interval_minutes=5,
    disruption_start=5
)


# ============================================================
# 3. RULE-BASED DETECTION
# ============================================================

detection_results = analyze_city(
    normal_data,
    current_data
)


# ============================================================
# 4. CREATE HISTORICAL ML FEATURES
# ============================================================

training_features = create_historical_ml_features(
    historical_data
)

print("\nHISTORICAL ML TRAINING RECORDS:")
print(len(training_features))


# ============================================================
# 5. TRAIN ML ANOMALY MODEL
# ============================================================

ml_model = train_anomaly_model(
    training_features
)


# ============================================================
# 6. ANALYZE EACH ZONE
# ============================================================

final_outputs = []


for zone_index, detection_result in enumerate(detection_results):

    zone_id = detection_result["zone_id"]


    # --------------------------------------------------------
    # Zone historical timeline
    # --------------------------------------------------------

    zone_history = [
        snapshot[zone_index]
        for snapshot in historical_data
    ]


    # --------------------------------------------------------
    # Change Point Detection
    # --------------------------------------------------------

    change_point_result = analyze_change_point(
        zone_history,
        threshold=10,
        minimum_signals=2
    )


    # --------------------------------------------------------
    # Early Warning Detection
    # --------------------------------------------------------

    early_warning_result = detect_early_warning(
        zone_history,
        change_threshold=5,
        minimum_signals=2
    )


    # --------------------------------------------------------
    # Recovery Detection
    # --------------------------------------------------------

    recovery_result = detect_recovery(
        zone_history,
        recovery_threshold=5,
        minimum_signals=2
    )


    # --------------------------------------------------------
    # Temporal Intelligence
    # --------------------------------------------------------

    temporal_features = create_temporal_features(
        zone_history,
        current_index=len(zone_history) - 1,
        window=3
    )

    temporal_result = analyze_temporal_state(
        temporal_features
    )


    # --------------------------------------------------------
    # Event Reconstruction
    # --------------------------------------------------------

    event_result = reconstruct_event(
        zone_history,
        temporal_result
    )


    # --------------------------------------------------------
    # Event Lifecycle
    # --------------------------------------------------------

    lifecycle_result = determine_event_lifecycle(
        event_result,
        temporal_result,
        recovery_result
    )


    # --------------------------------------------------------
    # ML Anomaly Detection
    # --------------------------------------------------------

    zone_ml_features = [
        record
        for record in training_features
        if record["zone_id"] == zone_id
    ]

    zone_latest_features = zone_ml_features[-1]


    zone_ml_result = predict_anomaly(
        ml_model,
        zone_latest_features
    )


    # --------------------------------------------------------
    # Historical Statistical Values
    # --------------------------------------------------------

    historical_values = {

        "rainfall": [
            snapshot[zone_index]["weather"]["rainfall_mm"]
            for snapshot in historical_data[:-1]
        ],

        "traffic": [
            snapshot[zone_index]["traffic"]["congestion_percent"]
            for snapshot in historical_data[:-1]
        ],

        "transit": [
            snapshot[zone_index]["transit"]["delay_minutes"]
            for snapshot in historical_data[:-1]
        ],

        "complaints": [
            snapshot[zone_index]["complaints"]["count"]
            for snapshot in historical_data[:-1]
        ]
    }


    # --------------------------------------------------------
    # Statistical Anomaly Detection
    # --------------------------------------------------------

    statistical_result = analyze_signal_statistics(
        current_data[zone_index],
        historical_values
    )


    statistical_anomaly = any(
        result["statistical_anomaly"]
        for result in statistical_result.values()
    )


    # --------------------------------------------------------
    # Ensemble Intelligence
    # --------------------------------------------------------

    ensemble_result = calculate_ensemble_result(

        rule_anomaly=detection_result["anomaly"],

        statistical_anomaly=statistical_anomaly,

        ml_anomaly=zone_ml_result["ml_anomaly"]
    )


    # ========================================================
    # PRINT ZONE INTELLIGENCE
    # ========================================================

    print("\n----------------------------------------")

    print("ZONE:", zone_id)


    print("\nSTATISTICAL INTELLIGENCE:")

    print(statistical_result)


    print("\nENSEMBLE INTELLIGENCE:")

    print(ensemble_result)


    print("\nEARLY WARNING INTELLIGENCE:")

    print(early_warning_result)


    print("\nCHANGE-POINT INTELLIGENCE:")

    print(change_point_result)


    print("\nRECOVERY INTELLIGENCE:")

    print(recovery_result)


    print("\nEVENT LIFECYCLE:")

    print(lifecycle_result)


    # ========================================================
    # BUILD FINAL INTELLIGENCE OUTPUT
    # ========================================================

    final_output = build_intelligence_output(

        zone_id=zone_id,

        detection_result=detection_result,

        temporal_result=temporal_result,

        event_result=event_result,

        ml_result=zone_ml_result,

        statistical_result=statistical_result,

        ensemble_result=ensemble_result,

        change_point_result=change_point_result,

        early_warning_result=early_warning_result,

        recovery_result=recovery_result,

        lifecycle_result=lifecycle_result
    )


    final_outputs.append(
        final_output
    )


# ============================================================
# FINAL CITYPULSE INTELLIGENCE OUTPUT
# ============================================================

print("\n")

print("=" * 60)

print(
    "       CITYPULSE — MEMBER 1 INTELLIGENCE OUTPUT"
)

print("=" * 60)


for output in final_outputs:

    print("\n----------------------------------------")

    print(
        "ZONE:",
        output["zone_id"]
    )

    print(
        "STATUS:",
        output["status"]
    )

    print(
        "RISK SCORE:",
        output["risk_score"]
    )

    print(
        "ANOMALY:",
        output["anomaly"]
    )


    print("\nSIGNALS DETECTED:")

    print(
        output["signals_detected"]
    )


    print("\nWHY FLAGGED:")

    print(
        output["why_flagged"]
    )


    print("\nML INTELLIGENCE:")

    print(
        output["ml"]
    )


    print("\nSTATISTICAL INTELLIGENCE:")

    print(
        output["statistical"]
    )


    print("\nENSEMBLE INTELLIGENCE:")

    print(
        output["ensemble"]
    )


    print("\nEARLY WARNING INTELLIGENCE:")

    print(
        output["early_warning"]
    )


    print("\nCHANGE-POINT INTELLIGENCE:")

    print(
        output["change_point"]
    )


    print("\nTEMPORAL INTELLIGENCE:")

    print(
        output["temporal"]
    )


    print("\nEVENT INTELLIGENCE:")

    print(
        output["event"]
    )


    print("\nRECOVERY INTELLIGENCE:")

    print(
        output["recovery"]
    )


    print("\nEVENT LIFECYCLE:")

    print(
        output["event_lifecycle"]
    )


# ============================================================
# SAVE FINAL JSON
# ============================================================

with open(
    "citypulse_output.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        final_outputs,
        file,
        indent=4,
        default=str
    )


print("\n")

print("=" * 60)

print(
    "MEMBER 1 PIPELINE COMPLETE"
)

print("=" * 60)

print("\nCityPulse intelligence output saved to:")

print("citypulse_output.json")