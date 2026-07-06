import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "data" / "logs"


def collect_windows_logs():
    with open(LOG_DIR / "windows_logs.json", "r") as file:
        return json.load(file)


def collect_linux_logs():
    with open(LOG_DIR / "linux_logs.log", "r") as file:
        return file.readlines()


def collect_firewall_logs():
    with open(LOG_DIR / "firewall.log", "r") as file:
        return file.readlines()