from tools import (
    investigate_zone,
    compare_zones,
    get_event_timeline,
    get_evidence,
    get_recovery_status
)

from simulation import simulate_zone_change


# =========================================================
# CITYPULSE CIVIC AI AGENT
# =========================================================

class CivicAIAgent:
    """
    CityPulse Civic AI Agent.

    The agent provides five core capabilities:

    1. Investigate
    2. Compare
    3. Verify
    4. Explain
    5. Simulate
    """

    def __init__(self):
        self.name = "CityPulse Civic AI Agent"

    # -----------------------------------------------------
    # INVESTIGATE
    # -----------------------------------------------------

    def investigate(self, zone_id):
        """
        Investigate the current condition of a zone.
        """

        return investigate_zone(zone_id)

    # -----------------------------------------------------
    # COMPARE
    # -----------------------------------------------------

    def compare(self, zone_id_1, zone_id_2):
        """
        Compare two civic zones.
        """

        return compare_zones(
            zone_id_1,
            zone_id_2
        )

    # -----------------------------------------------------
    # VERIFY
    # -----------------------------------------------------

    def verify(self, zone_id):
        """
        Verify the evidence behind a detected event.
        """

        return get_evidence(zone_id)

    # -----------------------------------------------------
    # EXPLAIN
    # -----------------------------------------------------

    def explain(self, zone_id):
        """
        Gather the evidence needed to explain
        what is happening in a zone.
        """

        investigation = investigate_zone(zone_id)

        evidence = get_evidence(zone_id)

        timeline = get_event_timeline(zone_id)

        recovery = get_recovery_status(zone_id)

        return {
            "zone_id": zone_id,
            "investigation": investigation,
            "evidence": evidence,
            "timeline": timeline,
            "recovery": recovery
        }

    # -----------------------------------------------------
    # SIMULATE
    # -----------------------------------------------------

    def simulate(
        self,
        zone_id,
        signal,
        percentage_change
    ):
        """
        Run a What-If simulation.
        """

        return simulate_zone_change(
            zone_id,
            signal,
            percentage_change
        )


# =========================================================
# BASIC TEST
# =========================================================

if __name__ == "__main__":

    agent = CivicAIAgent()

    print("CITYPULSE CIVIC AI AGENT TEST")
    print("=" * 50)

    print()
    print("Agent:", agent.name)

    print()
    print("Available capabilities:")
    print("- Investigate")
    print("- Compare")
    print("- Verify")
    print("- Explain")
    print("- Simulate")

    print()
    print("Agent initialized successfully.")