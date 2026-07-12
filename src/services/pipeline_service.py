import platform


def execute_pipeline():
    """
    Run the live Windows ingestion pipeline.

    This feature is available only when the application runs directly
    on Windows. The Docker web container runs Linux and therefore cannot
    access Windows Event Viewer through win32evtlog.
    """

    if platform.system() != "Windows":
        raise RuntimeError(
            "Live Windows log collection is available only on the "
            "Windows host, not inside the Linux Docker container."
        )

    # Import Windows-dependent modules only after confirming Windows.
    from src.database.insert_live_windows_logs import (
        insert_live_windows_logs,
    )
    from src.database.insert_alerts import insert_alerts
    from src.database.auto_incidents import (
        create_incidents_from_high_alerts,
    )

    print("=" * 60)
    print("SOC Pipeline Started")
    print("=" * 60)

    insert_live_windows_logs()
    print("✔ Live Windows logs collected")

    inserted_alerts = insert_alerts()
    print(f"✔ {inserted_alerts} new alerts saved")

    inserted_incidents = create_incidents_from_high_alerts()
    print(f"✔ {inserted_incidents} new incidents created")

    print("=" * 60)
    print("SOC Pipeline Finished")
    print("=" * 60)

    return {
        "alerts_created": inserted_alerts,
        "incidents_created": inserted_incidents,
    }


if __name__ == "__main__":
    execute_pipeline()