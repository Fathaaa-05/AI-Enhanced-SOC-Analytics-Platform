import win32evtlog


def map_severity(event_type):
    if event_type == 1:
        return "High"      # Error
    elif event_type == 2:
        return "Medium"    # Warning
    else:
        return "Low"       # Information


def collect_live_windows_logs(limit=20):
    server = "localhost"
    log_type = "System"

    hand = win32evtlog.OpenEventLog(server, log_type)

    flags = (
        win32evtlog.EVENTLOG_BACKWARDS_READ |
        win32evtlog.EVENTLOG_SEQUENTIAL_READ
    )

    events = win32evtlog.ReadEventLog(hand, flags, 0)

    logs = []

    for event in events[:limit]:
        logs.append({
            "timestamp": str(event.TimeGenerated),
            "source": "Windows-System",
            "username": "SYSTEM",
            "source_ip": "localhost",
            "event_type": "System Event",
            "status": event.SourceName,
            "severity": map_severity(event.EventType),
            "destination_port": None
        })

    return logs


if __name__ == "__main__":
    logs = collect_live_windows_logs(10)

    for log in logs:
        print(log)