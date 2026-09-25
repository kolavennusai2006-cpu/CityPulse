from datetime import datetime


ZONES = [
    "ZONE_A",
    "ZONE_B",
    "ZONE_C",
    "ZONE_D",
    "ZONE_E"
]


NORMAL_DATA = {
    "ZONE_A": {
        "rainfall_mm": 2.0,
        "traffic": 35,
        "transit": 5,
        "complaints": 10
    },

    "ZONE_B": {
        "rainfall_mm": 4.0,
        "traffic": 40,
        "transit": 6,
        "complaints": 12
    },

    "ZONE_C": {
        "rainfall_mm": 3.0,
        "traffic": 45,
        "transit": 7,
        "complaints": 8
    },

    "ZONE_D": {
        "rainfall_mm": 5.0,
        "traffic": 50,
        "transit": 5,
        "complaints": 10
    },

    "ZONE_E": {
        "rainfall_mm": 4.0,
        "traffic": 42,
        "transit": 6,
        "complaints": 9
    }
}


# ============================================================
# EXISTING SINGLE-SNAPSHOT GENERATOR
# ============================================================

def generate_zone_data(zone_id, disruption=False):

    if disruption and zone_id == "ZONE_A":

        rainfall = 18.5
        traffic = 82
        transit_delay = 24
        complaints = 38

    else:

        normal = NORMAL_DATA[zone_id]

        rainfall = normal["rainfall_mm"]
        traffic = normal["traffic"]
        transit_delay = normal["transit"]
        complaints = normal["complaints"]

    return {
        "zone_id": zone_id,

        "timestamp": datetime.now().isoformat(),

        "weather": {
            "rainfall_mm": rainfall
        },

        "traffic": {
            "congestion_percent": traffic
        },

        "transit": {
            "delay_minutes": transit_delay
        },

        "complaints": {
            "count": complaints
        }
    }


def generate_city_data(disruption=False):

    city_data = []

    for zone in ZONES:

        city_data.append(
            generate_zone_data(
                zone,
                disruption
            )
        )

    return city_data


# ============================================================
# HISTORICAL TIME-SERIES GENERATOR
# ============================================================

def generate_historical_data(
    num_snapshots=12,
    interval_minutes=5,
    disruption_start=5
):
    """
    Generate deterministic historical civic data.

    Zone A timeline:

    +00 to +20 : NORMAL

    +25         : EVENT START

    +30 to +40  : DEVELOPING

    +45 to +50  : PEAK

    +55         : RECOVERY

    Other zones remain normal.
    """

    history = []

    for snapshot in range(num_snapshots):

        city_snapshot = []

        for zone in ZONES:

            normal = NORMAL_DATA[zone]

            # --------------------------------------------
            # NORMAL BASELINE
            # --------------------------------------------

            rainfall = normal["rainfall_mm"]

            traffic = normal["traffic"]

            transit_delay = normal["transit"]

            complaints = normal["complaints"]


            # --------------------------------------------
            # ZONE A EVENT LIFECYCLE
            # --------------------------------------------

            if zone == "ZONE_A":

                # ========================================
                # NORMAL PHASE
                # ========================================

                if snapshot < disruption_start:

                    rainfall = 2.0

                    traffic = 35

                    transit_delay = 5

                    complaints = 10


                # ========================================
                # EVENT START
                # +25 MINUTES
                # ========================================

                elif snapshot == 5:

                    rainfall = 5.0

                    traffic = 43

                    transit_delay = 8

                    complaints = 15


                # ========================================
                # DEVELOPING
                # +30 MINUTES
                # ========================================

                elif snapshot == 6:

                    rainfall = 8.0

                    traffic = 51

                    transit_delay = 11

                    complaints = 20


                # ========================================
                # DEVELOPING
                # +35 MINUTES
                # ========================================

                elif snapshot == 7:

                    rainfall = 11.0

                    traffic = 59

                    transit_delay = 14

                    complaints = 25


                # ========================================
                # DEVELOPING
                # +40 MINUTES
                # ========================================

                elif snapshot == 8:

                    rainfall = 14.0

                    traffic = 67

                    transit_delay = 17

                    complaints = 30


                # ========================================
                # PEAK
                # +45 MINUTES
                # ========================================

                elif snapshot == 9:

                    rainfall = 20.0

                    traffic = 83

                    transit_delay = 23

                    complaints = 40


                # ========================================
                # PEAK
                # +50 MINUTES
                # ========================================

                elif snapshot == 10:

                    rainfall = 23.0

                    traffic = 91

                    transit_delay = 26

                    complaints = 45


                # ========================================
                # RECOVERY
                # +55 MINUTES
                # ========================================

                elif snapshot == 11:

                    rainfall = 15.0

                    traffic = 70

                    transit_delay = 18

                    complaints = 30


            # --------------------------------------------
            # CREATE SNAPSHOT
            # --------------------------------------------

            city_snapshot.append({

                "zone_id": zone,

                "snapshot_index": snapshot,

                "time_offset_minutes": (
                    snapshot * interval_minutes
                ),

                "weather": {

                    "rainfall_mm": round(
                        rainfall,
                        2
                    )

                },

                "traffic": {

                    "congestion_percent": traffic

                },

                "transit": {

                    "delay_minutes": transit_delay

                },

                "complaints": {

                    "count": complaints

                }

            })

        history.append(city_snapshot)

    return history


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # NORMAL CITY DATA TEST
    # --------------------------------------------------------

    print("NORMAL CITY DATA")

    print("=" * 60)

    normal_data = generate_city_data(
        disruption=False
    )

    for zone in normal_data:

        print(zone)


    # --------------------------------------------------------
    # DISRUPTION TEST
    # --------------------------------------------------------

    print("\nDISRUPTION SCENARIO")

    print("=" * 60)

    disruption_data = generate_city_data(
        disruption=True
    )

    for zone in disruption_data:

        print(zone)


    # --------------------------------------------------------
    # HISTORICAL DATA TEST
    # --------------------------------------------------------

    print("\n\nHISTORICAL DATA TEST")

    print("=" * 60)

    historical_data = generate_historical_data()

    for snapshot in historical_data:

        zone_a = snapshot[0]

        print(
            f"\nTIME +"
            f"{zone_a['time_offset_minutes']}"
            f" minutes"
        )

        print(
            "Zone A:",
            "Rainfall =",
            zone_a["weather"]["rainfall_mm"],
            "| Traffic =",
            zone_a["traffic"]["congestion_percent"],
            "| Transit =",
            zone_a["transit"]["delay_minutes"],
            "| Complaints =",
            zone_a["complaints"]["count"]
        )