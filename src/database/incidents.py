from src.database.mysql import get_connection


def create_incident(alert_id, priority="High", assigned_to="SOC Analyst"):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO incidents
    (alert_id, assigned_to, priority)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (alert_id, assigned_to, priority))

    connection.commit()
    cursor.close()
    connection.close()

    print("✅ Incident created successfully!")


def fetch_incidents():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            incidents.incident_id,
            alerts.attack,
            alerts.source_ip,
            alerts.severity,
            alerts.mitre_technique,
            incidents.assigned_to,
            incidents.priority,
            incidents.status,
            incidents.created_at
        FROM incidents
        JOIN alerts ON incidents.alert_id = alerts.alert_id
        ORDER BY incidents.created_at DESC
    """)

    incidents = cursor.fetchall()

    cursor.close()
    connection.close()

    return incidents