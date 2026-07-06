from collections import defaultdict

from src.database.fetch_logs import fetch_logs
from src.database.fetch_alerts import fetch_alerts
from src.database.incidents import fetch_incidents
from src.dashboard.ai_service import get_ai_anomalies


def calculate_risk_scores():

    logs = fetch_logs()
    alerts = fetch_alerts()
    incidents = fetch_incidents()
    ai_anomalies = get_ai_anomalies()

    risk = defaultdict(int)

    # Failed logins
    for log in logs:
         if log["username"] == "N/A":
            continue
         if log["status"] == "Failed Login":
            risk[log["username"]] += 1

    # High severity alerts
    for alert in alerts:
        for log in logs:
            if log["source_ip"] == alert["source_ip"]:
                risk[log["username"]] += 5

    # Open incidents
    for incident in incidents:
        for log in logs:
            if log["source_ip"] == incident["source_ip"]:
                risk[log["username"]] += 10

    # AI anomalies
    for anomaly in ai_anomalies:
        risk[anomaly["username"]] += 8

    results = []

max_score = max(risk.values()) if risk else 1

for user, raw_score in risk.items():

    if user == "N/A":
        continue

    score = int((raw_score / max_score) * 100)
    
    if score >= 80:
        level = "Critical"

    elif score >= 60:
        level = "High"

    elif score >= 30:
        level = "Medium"

    else:
        level = "Low"

    results.append({
        "username": user,
        "score": score,
        "level": level
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


if __name__ == "__main__":

    users = calculate_risk_scores()

    for user in users:
        print(user)