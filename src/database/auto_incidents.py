from src.database.mysql import get_connection


def create_incidents_from_high_alerts():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT alert_id, severity
        FROM alerts
        WHERE severity IN ('High', 'Critical')
        ORDER BY time_detected DESC
    """)

    alerts = cursor.fetchall()

    inserted = 0
    skipped = 0

    try:
        for alert in alerts:
            alert_id = alert["alert_id"]
            severity = alert["severity"]

            cursor.execute(
                """
                SELECT incident_id
                FROM incidents
                WHERE alert_id = %s
                LIMIT 1
                """,
                (alert_id,)
            )

            existing_incident = cursor.fetchone()

            if existing_incident:
                skipped += 1
                continue

            priority = "Critical" if severity == "Critical" else "High"

            cursor.execute(
                """
                INSERT INTO incidents
                (
                    alert_id,
                    assigned_to,
                    priority,
                    status
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    alert_id,
                    "SOC Analyst",
                    priority,
                    "Open"
                )
            )

            inserted += 1

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

    print(f"✅ {inserted} new incidents created.")
    print(f"⏭️ {skipped} existing incidents skipped.")

    return inserted


if __name__ == "__main__":
    create_incidents_from_high_alerts()