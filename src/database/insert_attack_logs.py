from src.database.mysql import get_connection
from src.generator.attack_simulator import simulate_brute_force


def insert_attack_logs():
    logs = simulate_brute_force()

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO logs
    (timestamp, source, username, source_ip, event_type, status, severity, destination_port)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for log in logs:
        cursor.execute(query, (
            log.get("timestamp"),
            log.get("source"),
            log.get("username"),
            log.get("source_ip"),
            log.get("event_type"),
            log.get("status"),
            log.get("severity"),
            log.get("destination_port")
        ))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"✅ {len(logs)} attack logs inserted into MySQL!")


if __name__ == "__main__":
    insert_attack_logs()