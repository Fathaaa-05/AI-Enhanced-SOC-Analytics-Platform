import json
import random
from datetime import datetime, timedelta
from pathlib import Path

from src.generator.sample_data import (
    USERS,
    SOURCES,
    EVENT_TYPES,
    LOGIN_STATUS,
    NETWORK_STATUS,
    random_ip
)

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = BASE_DIR / "data" / "generated" / "security_logs.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def generate_logs(count=5000):

    logs = []

    start = datetime.now() - timedelta(days=30)

    for _ in range(count):

        source = random.choice(SOURCES)
        event = random.choice(EVENT_TYPES)

        log = {
            "timestamp": (
                start +
                timedelta(minutes=random.randint(0, 40000))
            ).strftime("%Y-%m-%d %H:%M:%S"),

            "source": source,

            "username": random.choice(USERS),

            "source_ip": random_ip(),

            "event_type": event
        }

        if event == "Login":

            log["status"] = random.choice(LOGIN_STATUS)

        elif event == "Network Traffic":

            log["status"] = random.choice(NETWORK_STATUS)
            log["destination_port"] = random.choice(
                [22,23,25,53,80,110,443,445,3389,8080]
            )

        else:

            log["status"] = "File Open"

        if log["status"] in ["Failed Login","DENY"]:

            log["severity"] = "High"

        else:

            log["severity"] = "Low"

        logs.append(log)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    print(f"✅ Generated {count} logs")
    print(f"📁 Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_logs()