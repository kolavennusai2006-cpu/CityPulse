from tools import load_citypulse_data


# =========================================================
# SIGNAL THRESHOLDS
# =========================================================

SIGNAL_THRESHOLDS = {
    "rainfall_mm": 5,
    "traffic_percent": 30,
    "transit_delay_minutes": 5,
    "complaints_count": 10
}


# =========================================================
# STATUS
# =========================================================

def get_status(risk_score):
    if risk_score >= 75:
        return "CRITICAL"
    elif risk_score >= 50:
        return "EMERGING"
    elif risk_score >= 30:
        return "WATCH"
    else:
        return "NORMAL"


# =========================================================
# RECOMPUTE CIVIC STATE
# =========================================================

def recompute_civic_state(
    evidence,
    simulated_signal,
    simulated_value
):
    """
    Recompute the hypothetical civic state after
    changing one signal.

    This is a simulation only.
    It does not modify Member 1's observed data.
    """

    # Copy observed evidence
    state = {
        "rainfall_mm": evidence.get("rainfall_mm", 0),
        "traffic_percent": evidence.get("traffic_percent", 0),
        "transit_delay_minutes": evidence.get(
            "transit_delay_minutes", 0
        ),
        "complaints_count": evidence.get(
            "complaints_count", 0
        )
    }

    # Apply hypothetical change
    state[simulated_signal] = simulated_value

    return state


# =========================================================
# RECOMPUTE SIMULATED RISK
# =========================================================

def recompute_risk(civic_state):
    """
    Recompute hypothetical civic risk from the
    simulated civic state.

    Each active civic signal contributes 25 points.
    """

    active_signals = []

    if (
        civic_state["rainfall_mm"]
        >= SIGNAL_THRESHOLDS["rainfall_mm"]
    ):
        active_signals.append("HEAVY_RAIN")

    if (
        civic_state["traffic_percent"]
        >= SIGNAL_THRESHOLDS["traffic_percent"]
    ):
        active_signals.append("TRAFFIC_SPIKE")

    if (
        civic_state["transit_delay_minutes"]
        >= SIGNAL_THRESHOLDS["transit_delay_minutes"]
    ):
        active_signals.append("TRANSIT_DELAY")

    if (
        civic_state["complaints_count"]
        >= SIGNAL_THRESHOLDS["complaints_count"]
    ):
        active_signals.append("COMPLAINT_SPIKE")

    risk_score = min(
        len(active_signals) * 25,
        100
    )

    return {
        "risk_score": risk_score,
        "status": get_status(risk_score),
        "signals_detected": active_signals
    }


# =========================================================
# PROJECT CONSEQUENCES
# =========================================================

def project_consequences(
    current_state,
    simulated_state
):
    """
    Describe what changed between observed and
    simulated civic conditions.
    """

    changes = []

    for signal in current_state:

        before = current_state[signal]
        after = simulated_state[signal]

        if before != after:

            changes.append({
                "signal": signal,
                "observed_value": before,
                "simulated_value": after
            })

    return changes


# =========================================================
# WHAT-IF SIMULATION
# =========================================================

def simulate_zone_change(
    zone_id,
    signal,
    percentage_change
):
    """
    Layer 14: Simulation

    Flow:

        User What-If Input
                ↓
        Recompute civic state
                ↓
        Recompute risk
                ↓
        Projected consequences
                ↓
        SIMULATED — NOT OBSERVED
    """

    # -----------------------------------------------------
    # Load Member 1 intelligence
    # -----------------------------------------------------

    result = load_citypulse_data()

    if not result.get("success"):

        return {
            "success": False,
            "error": (
                "Unable to load CityPulse "
                "intelligence data."
            )
        }

    zones = result.get("data", [])

    # -----------------------------------------------------
    # Find zone
    # -----------------------------------------------------

    zone_data = None

    for zone in zones:

        if zone.get("zone_id") == zone_id:

            zone_data = zone
            break

    if zone_data is None:

        return {
            "success": False,
            "error": f"Zone {zone_id} not found."
        }

    # -----------------------------------------------------
    # Validate signal
    # -----------------------------------------------------

    valid_signals = list(
        SIGNAL_THRESHOLDS.keys()
    )

    if signal not in valid_signals:

        return {
            "success": False,
            "error": (
                f"Unsupported signal '{signal}'. "
                f"Valid signals: {valid_signals}"
            )
        }

    # -----------------------------------------------------
    # Get observed evidence
    # -----------------------------------------------------

    event_data = zone_data.get(
        "event",
        {}
    )

    evidence = event_data.get(
        "evidence",
        {}
    )

    current_value = evidence.get(signal)

    if current_value is None:

        return {
            "success": False,
            "error": (
                f"Signal '{signal}' has no "
                f"available evidence for {zone_id}."
            )
        }

    # -----------------------------------------------------
    # Calculate hypothetical value
    # -----------------------------------------------------

    simulated_value = (
        current_value
        * (1 + percentage_change / 100)
    )

    simulated_value = round(
        simulated_value,
        2
    )

    # -----------------------------------------------------
    # OBSERVED STATE
    # -----------------------------------------------------

    observed_state = {
        "rainfall_mm": evidence.get(
            "rainfall_mm",
            0
        ),
        "traffic_percent": evidence.get(
            "traffic_percent",
            0
        ),
        "transit_delay_minutes": evidence.get(
            "transit_delay_minutes",
            0
        ),
        "complaints_count": evidence.get(
            "complaints_count",
            0
        )
    }

    # -----------------------------------------------------
    # CURRENT OBSERVED RISK
    # -----------------------------------------------------

    observed_risk = zone_data.get(
        "risk_score",
        0
    )

    observed_status = zone_data.get(
        "status",
        "NORMAL"
    )

    # -----------------------------------------------------
    # RECOMPUTE CIVIC STATE
    # -----------------------------------------------------

    simulated_state = recompute_civic_state(
        observed_state,
        signal,
        simulated_value
    )

    # -----------------------------------------------------
    # RECOMPUTE RISK
    # -----------------------------------------------------

    simulated_risk = recompute_risk(
        simulated_state
    )

    # -----------------------------------------------------
    # PROJECT CONSEQUENCES
    # -----------------------------------------------------

    consequences = project_consequences(
        observed_state,
        simulated_state
    )

    # -----------------------------------------------------
    # Risk difference
    # -----------------------------------------------------

    risk_change = (
        simulated_risk["risk_score"]
        - observed_risk
    )

    # -----------------------------------------------------
    # Interpretation
    # -----------------------------------------------------

    if risk_change > 0:

        interpretation = (
            f"The hypothetical change in {signal} "
            f"increases the recomputed civic risk "
            f"from {observed_risk} to "
            f"{simulated_risk['risk_score']}."
        )

    elif risk_change < 0:

        interpretation = (
            f"The hypothetical change in {signal} "
            f"decreases the recomputed civic risk "
            f"from {observed_risk} to "
            f"{simulated_risk['risk_score']}."
        )

    else:

        interpretation = (
            f"The hypothetical change in {signal} "
            f"does not change the recomputed civic "
            f"risk score, which remains "
            f"{observed_risk}."
        )

    # -----------------------------------------------------
    # FINAL SIMULATION RESULT
    # -----------------------------------------------------

    return {

        "success": True,

        "simulation_type": (
            "WHAT_IF"
        ),

        "observed_or_simulated": (
            "SIMULATED — NOT OBSERVED"
        ),

        "zone_id": zone_id,

        "input": {
            "signal": signal,
            "percentage_change": percentage_change
        },

        "signal_change": {
            "observed_value": current_value,
            "simulated_value": simulated_value
        },

        "observed_state": {
            "risk_score": observed_risk,
            "status": observed_status,
            "signals_detected": (
                zone_data.get(
                    "signals_detected",
                    []
                )
            )
        },

        "simulated_state": {
            "civic_state": simulated_state,
            "risk_score": simulated_risk[
                "risk_score"
            ],
            "status": simulated_risk[
                "status"
            ],
            "signals_detected": simulated_risk[
                "signals_detected"
            ]
        },

        "risk_change": risk_change,

        "projected_consequences": consequences,

        "interpretation": interpretation
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    result = simulate_zone_change(
        "ZONE_A",
        "rainfall_mm",
        30
    )

    print(
        "WHAT-IF SIMULATION TEST"
    )

    print("=" * 50)

    if result["success"]:

        print(
            "Simulation:",
            result["observed_or_simulated"]
        )

        print(
            "Zone:",
            result["zone_id"]
        )

        print(
            "Signal:",
            result["input"]["signal"]
        )

        print(
            "Change:",
            result["input"][
                "percentage_change"
            ],
            "%"
        )

        print()

        print(
            "OBSERVED STATE"
        )

        print(
            "Risk:",
            result["observed_state"][
                "risk_score"
            ]
        )

        print(
            "Status:",
            result["observed_state"][
                "status"
            ]
        )

        print()

        print(
            "SIMULATED STATE"
        )

        print(
            "Original value:",
            result["signal_change"][
                "observed_value"
            ]
        )

        print(
            "Simulated value:",
            result["signal_change"][
                "simulated_value"
            ]
        )

        print(
            "Risk:",
            result["simulated_state"][
                "risk_score"
            ]
        )

        print(
            "Status:",
            result["simulated_state"][
                "status"
            ]
        )

        print(
            "Signals:",
            result["simulated_state"][
                "signals_detected"
            ]
        )

        print()

        print(
            "Risk change:",
            result["risk_change"]
        )

        print()

        print(
            "Projected consequences:"
        )

        for consequence in result[
            "projected_consequences"
        ]:

            print(
                "-",
                consequence["signal"],
                ":",
                consequence["observed_value"],
                "→",
                consequence["simulated_value"]
            )

        print()

        print(
            "Interpretation:"
        )

        print(
            result["interpretation"]
        )

        print()

        print(
            "SIMULATED — NOT OBSERVED"
        )

    else:

        print(
            "Simulation failed."
        )

        print(
            "Error:",
            result["error"]
        )