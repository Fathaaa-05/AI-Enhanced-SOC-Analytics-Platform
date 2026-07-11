import win32evtlog


SECURITY_EVENTS = {
    4624: {
        "status": "Successful Login",
        "event_type": "Login",
        "severity": "Low"
    },
    4625: {
        "status": "Failed Login",
        "event_type": "Login",
        "severity": "High"
    },
    4672: {
        "status": "Special Privileges Assigned",
        "event_type": "Privilege Activity",
        "severity": "High"
    },
    4720: {
        "status": "User Account Created",
        "event_type": "Account Management",
        "severity": "High"
    },
    4726: {
        "status": "User Account Deleted",
        "event_type": "Account Management",
        "severity": "High"
    }
}


def collect_live_windows_logs(limit=20):
    server = "localhost"
    log_type = "Security"

    handle = win32evtlog.OpenEventLog(server, log_type)

    flags = (
        win32evtlog.EVENTLOG_BACKWARDS_READ
        | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    )

    events = win32evtlog.ReadEventLog(handle, flags, 0)

    logs = []

    for event in events:
        event_id = event.EventID & 0xFFFF

        if event_id not in SECURITY_EVENTS:
            continue

        mapping = SECURITY_EVENTS[event_id]

        username = "N/A"

        if event.StringInserts:
            try:
                username = str(event.StringInserts[5])
            except (IndexError, TypeError):
                username = "N/A"

        logs.append({
            "timestamp": str(event.TimeGenerated),
            "event_id": str(event_id),
            "source": "Windows-Security",
            "username": username,
            "source_ip": "localhost",
            "event_type": mapping["event_type"],
            "status": mapping["status"],
            "severity": mapping["severity"],
            "destination_port": None
        })

        if len(logs) >= limit:
            break

    win32evtlog.CloseEventLog(handle)

    return logs


if __name__ == "__main__":
    logs = collect_live_windows_logs(20)

    print(f"Collected Security Events: {len(logs)}")

    for log in logs:
        print(log)