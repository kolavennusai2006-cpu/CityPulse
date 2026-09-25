from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "rainfall_mm",
    "traffic_percent",
    "transit_delay_minutes",
    "complaints_count",
    "rainfall_change",
    "traffic_change",
    "transit_change",
    "complaints_change",
    "signals_detected_count",
    "signal_convergence"
]


def train_anomaly_model(feature_records):
    """
    Train an Isolation Forest model using civic feature records.
    """

    X = [
        [record[column] for column in FEATURE_COLUMNS]
        for record in feature_records
    ]

    model = IsolationForest(
        contamination="auto",
        random_state=42
    )

    model.fit(X)

    return model


def predict_anomaly(model, feature_record):
    """
    Predict whether one civic state is anomalous.
    """

    X = [[feature_record[column] for column in FEATURE_COLUMNS]]

    prediction = model.predict(X)[0]
    anomaly_score = model.decision_function(X)[0]

    return {
        "ml_anomaly":bool(prediction == -1),
        "ml_score": round(float(anomaly_score), 4)
    }
if __name__ == "__main__":
    from generator import generate_city_data
    from detection import detect_signal_changes
    from features import create_features

    print("CITYPULSE ML ENGINE TEST")
    print("=" * 60)

    baseline_data = generate_city_data(disruption=False)
    current_data = generate_city_data(disruption=True)

    feature_records = []

    for baseline, current in zip(baseline_data, current_data):

        signal_changes = detect_signal_changes(
            current,
            baseline
        )

        features = create_features(
            current,
            baseline,
            signal_changes
        )

        feature_records.append(features)

    model = train_anomaly_model(feature_records)

    for features in feature_records:

        result = predict_anomaly(
            model,
            features
        )

        print("\nML RESULT")
        print("Anomaly:", result["ml_anomaly"])
        print("Score:", result["ml_score"])