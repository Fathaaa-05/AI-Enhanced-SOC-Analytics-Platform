from src.detection.brute_force import detect_brute_force
from src.detection.port_scan import detect_port_scan


def run_detection_engine():
    alerts = []

    # Run all detection modules
    alerts.extend(detect_brute_force())
    alerts.extend(detect_port_scan())

    return alerts


if __name__ == "__main__":
    alerts = run_detection_engine()

    print("=" * 60)
    print(" SOC Detection Engine")
    print("=" * 60)

    if alerts:
        for i, alert in enumerate(alerts, start=1):
            print(f"\nAlert #{i}")
            for key, value in alert.items():
                print(f"{key}: {value}")
    else:
        print("No threats detected.")