from src.parser.parser import get_all_normalized_logs


def detect_brute_force():
    logs = get_all_normalized_logs()
    failed_attempts = {}
    alerts = []

    for log in logs:
        if log["event_type"] == "Login" and log["status"] == "Failed Login":
            ip = log["source_ip"]

            if ip not in failed_attempts:
                failed_attempts[ip] = 0

            failed_attempts[ip] += 1

            if failed_attempts[ip] >= 2:
                alerts.append({
                    "attack": "Brute Force Attack",
                    "source_ip": ip,
                    "severity": "High",
                    "description": "Multiple failed login attempts detected from same IP",
                    "mitre_technique": "T1110 - Brute Force"
                })

    return alerts


if __name__ == "__main__":
    alerts = detect_brute_force()

    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("No brute force attack detected.")