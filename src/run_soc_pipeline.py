from src.database.insert_attack_logs import insert_attack_logs
from src.database.insert_alerts import insert_alerts


def run_pipeline():

    print("=" * 60)
    print("🚀 Starting AI-Enhanced SOC Pipeline")
    print("=" * 60)

    print("\n[1/2] Inserting attack logs...")
    insert_attack_logs()

    print("\n[2/2] Running detection engine...")
    insert_alerts()

    print("\n✅ SOC Pipeline Completed Successfully!")


if __name__ == "__main__":
    run_pipeline()