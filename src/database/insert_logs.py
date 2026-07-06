from src.database.mysql import get_connection
from src.parser.parser import get_all_normalized_logs


def insert_logs():
    logs = get_all_normalized_logs()
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO logs
    (timestamp, source, username, source_ip, event_type, status, severity, destination_port)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for log in logs:
        values = (
            log.get("timestamp"),
            log.get("source"),
            log.get("username"),
            log.get("source_ip"),
            log.get("event_type"),
            log.get("status"),
            log.get("severity"),
            log.get("destination_port")
        )

        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"✅ {len(logs)} logs inserted successfully!")


if __name__ == "__main__":
    insert_logs()