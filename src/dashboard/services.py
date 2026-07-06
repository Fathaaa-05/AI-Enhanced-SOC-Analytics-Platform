from src.database.fetch_logs import fetch_logs
from src.database.fetch_alerts import fetch_alerts
from src.dashboard.ai_service import get_ai_anomalies

def get_dashboard_data():
    ai_anomalies = get_ai_anomalies()
    logs = fetch_logs()
    alerts = fetch_alerts()

    total_logs = len(logs)
    total_alerts = len(alerts)

    high_alerts = len(
        [alert for alert in alerts if alert["severity"] == "High"]
    )

    medium_alerts = len(
        [alert for alert in alerts if alert["severity"] == "Medium"]
    )

    low_alerts = len(
        [alert for alert in alerts if alert["severity"] == "Low"]
    )

    return {
        "logs": logs,
        "alerts": alerts,
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "low_alerts": low_alerts,
        "ai_anomalies": ai_anomalies
    }