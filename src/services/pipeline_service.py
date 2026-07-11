from src.database.insert_live_windows_logs import insert_live_windows_logs
from src.database.insert_alerts import insert_alerts
from src.database.auto_incidents import create_incidents_from_high_alerts


def execute_pipeline():
    print("=" * 60)
    print("SOC Pipeline Started")
    print("=" * 60)

    insert_live_windows_logs()
    print("✔ Live Windows logs collected")

    inserted_alerts = insert_alerts()
    print(f"✔ {inserted_alerts} new alerts saved")

    inserted_incidents = create_incidents_from_high_alerts()
    print(f"✔ {inserted_incidents} new incidents created")

    print("=" * 60)
    print("SOC Pipeline Finished")
    print("=" * 60)

    return {
        "alerts_created": inserted_alerts,
        "incidents_created": inserted_incidents
    }


if __name__ == "__main__":
    execute_pipeline()