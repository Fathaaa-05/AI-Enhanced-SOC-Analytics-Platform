from src.database.fetch_logs import fetch_logs


def detect_privilege_escalation():
    alerts = []
    logs = fetch_logs()

    for log in logs:
        event_id = str(log.get("event_id", ""))
        status = str(log.get("status", ""))

        if (
            event_id == "4672"
            or "special privileges assigned" in status.lower()
        ):
            alerts.append({
                "attack": "Privileged Logon Detected",
                "source_ip": log.get("source_ip", "localhost"),
                "severity": "High",
                "mitre_technique": "T1078 - Valid Accounts"
            })

    return alerts


if __name__ == "__main__":
    detected_alerts = detect_privilege_escalation()

    print(f"Detected alerts: {len(detected_alerts)}")

    for alert in detected_alerts:
        print(alert)