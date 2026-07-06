import json
from pathlib import Path
from src.database.mysql import get_connection

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "generated" / "security_logs.json"


def insert_generated_logs():
    with open(INPUT_FILE, "r") as file:
        logs = json.load(file)

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

    print(f"✅ {len(logs)} generated logs inserted into MySQL!")


if __name__ == "__main__":
    insert_generated_logs()