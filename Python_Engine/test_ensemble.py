from ensemble_engine import calculate_ensemble_result


print("\nCITYPULSE — ENSEMBLE ANOMALY TEST")
print("=" * 50)


result = calculate_ensemble_result(
    rule_anomaly=True,
    statistical_anomaly=True,
    ml_anomaly=True
)


print("\nENSEMBLE RESULT:")
print(result)