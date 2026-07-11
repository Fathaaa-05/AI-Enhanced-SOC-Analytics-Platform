from src.database.mysql import get_connection
from src.detection.detection_engine import run_detection_engine


def insert_alerts():
    alerts = run_detection_engine()

    if not alerts:
        print("✅ Detection finished. No new alerts found.")
        return 0

    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO alerts
        (
            attack,
            source_ip,
            severity,
            mitre_technique,
            description
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    duplicate_query = """
        SELECT alert_id
        FROM alerts
        WHERE attack = %s
          AND source_ip = %s
          AND mitre_technique = %s
        LIMIT 1
    """

    inserted = 0
    skipped = 0

    try:
        for alert in alerts:
            attack = alert.get("attack", "Unknown Attack")
            source_ip = alert.get("source_ip", "N/A")
            severity = alert.get("severity", "Medium")
            mitre_technique = alert.get(
                "mitre_technique",
                "Unmapped"
            )

            description = alert.get(
                "description",
                (
                    f"{attack} detected from {source_ip}. "
                    f"Mapped to {mitre_technique}."
                )
            )

            # Check whether this alert already exists.
            cursor.execute(
                duplicate_query,
                (
                    attack,
                    source_ip,
                    mitre_technique
                )
            )

            existing_alert = cursor.fetchone()

            if existing_alert:
                skipped += 1
                continue

            cursor.execute(
                insert_query,
                (
                    attack,
                    source_ip,
                    severity,
                    mitre_technique,
                    description
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

    print(f"✅ {inserted} new alerts inserted.")
    print(f"⏭️ {skipped} duplicate alerts skipped.")

    return inserted


if __name__ == "__main__":
    insert_alerts()