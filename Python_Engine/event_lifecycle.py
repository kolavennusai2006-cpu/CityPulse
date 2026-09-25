def determine_event_lifecycle(
    event_result,
    temporal_result,
    recovery_result
):
    """
    Determine the current lifecycle stage of a civic event.

    Possible stages:
    EARLY_WARNING
    EVENT_START
    DEVELOPING
    PEAK
    RECOVERY
    RESOLVED
    NORMAL
    """

    event_detected = event_result.get("event_detected", False)
    recovery_detected = recovery_result.get("recovery_detected", False)

    temporal_state = temporal_result.get(
        "temporal_state",
        "STABLE"
    )

    if not event_detected and not recovery_detected:
        return {
            "lifecycle_stage": "NORMAL",
            "event_active": False,
            "recovery_active": False,
            "reason": "No active civic disruption detected."
        }

    # Recovery takes priority over developing/peak
    if recovery_detected:
        recovery_level = recovery_result.get(
            "recovery_level",
            "NONE"
        )

        if recovery_level == "HIGH":
            return {
                "lifecycle_stage": "RECOVERY",
                "event_active": True,
                "recovery_active": True,
                "reason": (
                    "Multiple civic signals are decreasing "
                    "after the detected disruption."
                )
            }

        return {
            "lifecycle_stage": "RECOVERY",
            "event_active": True,
            "recovery_active": True,
            "reason": (
                "Civic signals are showing signs of recovery."
            )
        }

    if temporal_state == "PEAK":
        return {
            "lifecycle_stage": "PEAK",
            "event_active": True,
            "recovery_active": False,
            "reason": (
                "Multiple civic signals have reached "
                "their highest disruption state."
            )
        }

    if temporal_state == "DEVELOPING":
        return {
            "lifecycle_stage": "DEVELOPING",
            "event_active": True,
            "recovery_active": False,
            "reason": (
                "The civic disruption is continuing "
                "to develop across multiple signals."
            )
        }

    if event_detected:
        return {
            "lifecycle_stage": "EVENT_START",
            "event_active": True,
            "recovery_active": False,
            "reason": (
                "A multi-signal civic disruption "
                "has been detected."
            )
        }

    return {
        "lifecycle_stage": "EARLY_WARNING",
        "event_active": False,
        "recovery_active": False,
        "reason": (
            "Multiple signals show early signs "
            "of potential disruption."
        )
    }