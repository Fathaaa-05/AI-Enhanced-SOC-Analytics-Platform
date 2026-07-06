from src.database.mysql import get_connection


def fetch_alerts():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY time_detected DESC
    """)

    alerts = cursor.fetchall()

    cursor.close()
    connection.close()

    return alerts


if __name__ == "__main__":
    alerts = fetch_alerts()

    print(f"Total Alerts: {len(alerts)}")

    for alert in alerts:
        print(alert)