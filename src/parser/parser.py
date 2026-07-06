import re
from src.collector.collect_logs import (
    collect_windows_logs,
    collect_linux_logs,
    collect_firewall_logs
)


def parse_windows_logs():
    logs = collect_windows_logs()
    normalized_logs = []

    for log in logs:
        normalized_logs.append({
            "timestamp": log["timestamp"],
            "source": "Windows",
            "username": log["username"],
            "source_ip": log["source_ip"],
            "event_type": "Login",
            "status": log["status"],
            "severity": "High" if log["status"] == "Failed Login" else "Low"
        })

    return normalized_logs


def parse_linux_logs():
    logs = collect_linux_logs()
    normalized_logs = []

    for line in logs:
        match = re.search(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (Failed|Accepted) password for (\w+) from ([\d.]+)",
            line
        )

        if match:
            timestamp, action, username, ip = match.groups()

            normalized_logs.append({
                "timestamp": timestamp,
                "source": "Linux",
                "username": username,
                "source_ip": ip,
                "event_type": "Login",
                "status": "Failed Login" if action == "Failed" else "Successful Login",
                "severity": "High" if action == "Failed" else "Low"
            })

    return normalized_logs


def parse_firewall_logs():
    logs = collect_firewall_logs()
    normalized_logs = []

    for line in logs:
        match = re.search(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (ALLOW|DENY) TCP ([\d.]+) (\d+)",
            line
        )

        if match:
            timestamp, action, ip, port = match.groups()

            normalized_logs.append({
                "timestamp": timestamp,
                "source": "Firewall",
                "username": "N/A",
                "source_ip": ip,
                "event_type": "Network Traffic",
                "status": action,
                "destination_port": port,
                "severity": "Medium" if action == "DENY" else "Low"
            })

    return normalized_logs


def get_all_normalized_logs():
    return parse_windows_logs() + parse_linux_logs() + parse_firewall_logs()


if __name__ == "__main__":
    logs = get_all_normalized_logs()

    for log in logs:
        print(log)