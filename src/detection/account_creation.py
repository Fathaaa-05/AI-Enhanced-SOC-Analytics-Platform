from src.database.fetch_logs import fetch_logs


def detect_account_creation():
    alerts = []
    logs = fetch_logs()

    for log in logs:
        event_id = str(log.get("event_id", ""))
        status = str(log.get("status", ""))

        if event_id == "4720" or "user account created" in status.lower():
            alerts.append({
                "attack": "Suspicious Account Creation",
                "source_ip": log.get("source_ip", "localhost"),
                "severity": "High",
                "mitre_technique": "T1136 - Create Account"
            })

    return alerts


if __name__ == "__main__":
    results = detect_account_creation()

    for alert in results:
        print(alert)