from src.database.mysql import get_connection


def fetch_incident_details(incident_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                incidents.incident_id,
                incidents.alert_id,
                incidents.assigned_to,
                incidents.priority,
                incidents.status,
                incidents.created_at,
                incidents.resolved_at,
                incidents.notes,
                alerts.attack,
                alerts.source_ip,
                alerts.severity,
                alerts.mitre_technique,
                alerts.description,
                alerts.time_detected
            FROM incidents
            JOIN alerts
                ON incidents.alert_id = alerts.alert_id
            WHERE incidents.incident_id = %s
            LIMIT 1
            """,
            (incident_id,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    incident = fetch_incident_details(1)
    print(incident)