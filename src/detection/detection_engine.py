from src.detection.privilege_escalation import detect_privilege_escalation
from src.detection.brute_force import detect_brute_force
from src.detection.port_scan import detect_port_scan
from src.detection.account_creation import detect_account_creation


def run_detection_engine():
    alerts = []

    alerts.extend(detect_privilege_escalation())
    alerts.extend(detect_brute_force())
    alerts.extend(detect_port_scan())
    alerts.extend(detect_account_creation())

    return alerts


if __name__ == "__main__":
    alerts = run_detection_engine()

    print("=" * 60)
    print("SOC Detection Engine")
    print("=" * 60)

    if alerts:
        for index, alert in enumerate(alerts, start=1):
            print(f"\nAlert #{index}")

            for key, value in alert.items():
                print(f"{key}: {value}")
    else:
        print("No threats detected.")