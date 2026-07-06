from src.parser.parser import get_all_normalized_logs


def detect_port_scan():
    logs = get_all_normalized_logs()

    scanned_ports = {}
    alerts = []

    for log in logs:

        if log["source"] == "Firewall":

            ip = log["source_ip"]
            port = log.get("destination_port")

            if ip not in scanned_ports:
                scanned_ports[ip] = set()

            scanned_ports[ip].add(port)

    for ip, ports in scanned_ports.items():

        if len(ports) >= 5:

            alerts.append({
                "attack": "Port Scan",
                "source_ip": ip,
                "ports_scanned": list(ports),
                "severity": "High",
                "description": "Multiple destination ports scanned from same IP.",
                "mitre_technique": "T1046 - Network Service Discovery"
            })

    return alerts


if __name__ == "__main__":

    alerts = detect_port_scan()

    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("No Port Scan Detected.")