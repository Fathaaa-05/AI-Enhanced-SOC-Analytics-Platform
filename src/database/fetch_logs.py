from src.database.mysql import get_connection


def fetch_logs():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return logs


if __name__ == "__main__":
    logs = fetch_logs()

    print(f"Total Logs: {len(logs)}")

    for log in logs:
        print(log)