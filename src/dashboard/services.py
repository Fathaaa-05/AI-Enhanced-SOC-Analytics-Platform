from src.database.fetch_logs import fetch_logs
from src.database.fetch_alerts import fetch_alerts
from src.database.incidents import fetch_incidents
from src.dashboard.ai_service import get_ai_anomalies
from src.ai.risk_engine import calculate_risk_scores


def get_dashboard_data():
    logs = fetch_logs()
    alerts = fetch_alerts()
    incidents = fetch_incidents()
    ai_anomalies = get_ai_anomalies()
    risk_users = calculate_risk_scores()

    total_logs = len(logs)
    total_alerts = len(alerts)
    total_incidents = len(incidents)

    high_alerts = len([alert for alert in alerts if alert["severity"] == "High"])
    medium_alerts = len([alert for alert in alerts if alert["severity"] == "Medium"])
    low_alerts = len([alert for alert in alerts if alert["severity"] == "Low"])

    critical_users = len([user for user in risk_users if user["level"] == "Critical"])

    return {
        "logs": logs,
        "alerts": alerts,
        "incidents": incidents,
        "ai_anomalies": ai_anomalies,
        "risk_users": risk_users,
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "total_incidents": total_incidents,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "low_alerts": low_alerts,
        "critical_users": critical_users
    }