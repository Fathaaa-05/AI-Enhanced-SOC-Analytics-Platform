from src.collector.windows_live import collect_live_windows_logs
from src.database.mysql import get_connection


def insert_live_windows_logs():
    logs = collect_live_windows_logs(20)

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO logs
    (timestamp, event_id, source, username, source_ip, event_type, status, severity, destination_port)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for log in logs:
        cursor.execute(query, (
            log["timestamp"],
            log["event_id"],
            log["source"],
            log["username"],
            log["source_ip"],
            log["event_type"],
            log["status"],
            log["severity"],
            log["destination_port"]
        ))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"✅ {len(logs)} live Windows logs inserted into MySQL!")


if __name__ == "__main__":
    insert_live_windows_logs()