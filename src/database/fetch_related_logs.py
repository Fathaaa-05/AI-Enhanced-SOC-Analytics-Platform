from src.database.mysql import get_connection


def fetch_related_logs(source_ip, limit=20):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            timestamp,
            event_id,
            username,
            source_ip,
            event_type,
            status,
            severity
        FROM logs
        WHERE source_ip=%s
        ORDER BY timestamp DESC
        LIMIT %s
    """

    cursor.execute(query, (source_ip, limit))

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return logs


if __name__ == "__main__":
    logs = fetch_related_logs("localhost")

    for log in logs:
        print(log)