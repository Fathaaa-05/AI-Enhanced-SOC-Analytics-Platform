from src.database.mysql import get_connection
from src.detection.detection_engine import run_detection_engine


def insert_alerts():
    alerts = run_detection_engine()

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO alerts
    (attack, source_ip, severity, mitre_technique, description)
    VALUES (%s,%s,%s,%s,%s)
    """

    inserted = 0

    for alert in alerts:
        cursor.execute(query, (
            alert["attack"],
            alert["source_ip"],
            alert["severity"],
            alert["mitre_technique"],
            alert["description"]
        ))
        inserted += 1

    connection.commit()
    cursor.close()
    connection.close()

    print(f"✅ {inserted} new alerts inserted.")


if __name__ == "__main__":
    insert_alerts()