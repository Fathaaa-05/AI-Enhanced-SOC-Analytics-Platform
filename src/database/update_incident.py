from src.database.mysql import get_connection


ALLOWED_STATUSES = {
    "Open",
    "Investigating",
    "Resolved",
    "Closed",
}


def update_incident(
    incident_id,
    notes,
    status,
    assigned_to,
):
    if status not in ALLOWED_STATUSES:
        raise ValueError("Invalid incident status")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        if status in {"Resolved", "Closed"}:
            query = """
                UPDATE incidents
                SET notes = %s,
                    status = %s,
                    assigned_to = %s,
                    resolved_at = COALESCE(
                        resolved_at,
                        CURRENT_TIMESTAMP
                    )
                WHERE incident_id = %s
            """
        else:
            query = """
                UPDATE incidents
                SET notes = %s,
                    status = %s,
                    assigned_to = %s,
                    resolved_at = NULL
                WHERE incident_id = %s
            """

        cursor.execute(
            query,
            (
                notes,
                status,
                assigned_to,
                incident_id,
            ),
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()