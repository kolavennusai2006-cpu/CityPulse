from event_lifecycle import determine_event_lifecycle


event_result = {
    "event_detected": True
}

temporal_result = {
    "temporal_state": "DEVELOPING"
}

recovery_result = {
    "recovery_detected": True,
    "recovery_level": "HIGH"
}


result = determine_event_lifecycle(
    event_result,
    temporal_result,
    recovery_result
)


print("\nCITYPULSE — EVENT LIFECYCLE TEST")
print("=" * 50)

print("LIFECYCLE STAGE:")
print(result["lifecycle_stage"])

print("\nEVENT ACTIVE:")
print(result["event_active"])

print("\nRECOVERY ACTIVE:")
print(result["recovery_active"])

print("\nREASON:")
print(result["reason"])