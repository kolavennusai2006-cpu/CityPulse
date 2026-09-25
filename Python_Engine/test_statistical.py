from statistical_engine import analyze_signal_statistics


current = {
    "weather": {
        "rainfall_mm": 18
    },
    "traffic": {
        "congestion_percent": 82
    },
    "transit": {
        "delay_minutes": 24
    },
    "complaints": {
        "count": 38
    }
}


historical_values = {
    "rainfall": [
        2, 2, 2, 2, 2,
        3, 2, 2, 3, 2
    ],

    "traffic": [
        35, 36, 34, 37, 35,
        36, 35, 34, 36, 35
    ],

    "transit": [
        5, 5, 6, 5, 5,
        6, 5, 5, 6, 5
    ],

    "complaints": [
        10, 11, 9, 10, 10,
        11, 10, 9, 10, 11
    ]
}


results = analyze_signal_statistics(
    current,
    historical_values
)


print("\nCITYPULSE — STATISTICAL ANOMALY TEST")
print("=" * 50)

for signal, result in results.items():

    print("\n", signal.upper())
    print("Z-Score:", result["z_score"])
    print(
        "Statistical Anomaly:",
        result["statistical_anomaly"]
    )