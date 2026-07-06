from datetime import datetime, timedelta
import random

from src.generator.attack_profiles import USER_PROFILES


def simulate_brute_force():
    logs = []

    attacker_ip = "192.168.1.200"
    target_user = "admin"
    start_time = datetime.now().replace(hour=2, minute=10, second=0)

    for i in range(6):
        logs.append({
            "timestamp": (start_time + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "Windows",
            "username": target_user,
            "source_ip": attacker_ip,
            "event_type": "Login",
            "status": "Failed Login",
            "severity": "High"
        })

    logs.append({
        "timestamp": (start_time + timedelta(minutes=7)).strftime("%Y-%m-%d %H:%M:%S"),
        "source": "Windows",
        "username": target_user,
        "source_ip": attacker_ip,
        "event_type": "Login",
        "status": "Successful Login",
        "severity": "Medium"
    })

    return logs


def simulate_port_scan():
    pass


def simulate_impossible_travel():
    pass


def simulate_privilege_escalation():
    pass


def simulate_malware():
    pass


if __name__ == "__main__":
    brute_force_logs = simulate_brute_force()

    for log in brute_force_logs:
        print(log)