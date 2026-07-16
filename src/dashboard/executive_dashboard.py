from src.database.mysql import get_connection


def get_executive_summary():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    summary = {}

    try:
        # Total logs
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM logs
        """)
        summary["total_logs"] = cursor.fetchone()["total"]

        # Open incidents
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM incidents
            WHERE status NOT IN ('Resolved', 'Closed')
        """)
        summary["open_incidents"] = cursor.fetchone()["total"]

        # Completed incidents
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM incidents
            WHERE status IN ('Resolved', 'Closed')
        """)
        summary["resolved_incidents"] = cursor.fetchone()["total"]

        # Most common attack
        cursor.execute("""
            SELECT
                attack,
                COUNT(*) AS total
            FROM alerts
            WHERE attack IS NOT NULL
              AND attack != ''
            GROUP BY attack
            ORDER BY total DESC
            LIMIT 1
        """)

        attack = cursor.fetchone()

        summary["top_attack"] = (
            attack["attack"]
            if attack
            else "None"
        )

        # Most targeted user
        cursor.execute("""
            SELECT
                username,
                COUNT(*) AS total
            FROM logs
            WHERE username IS NOT NULL
              AND username != ''
              AND username NOT IN ('N/A', 'SYSTEM')
            GROUP BY username
            ORDER BY total DESC
            LIMIT 1
        """)

        user = cursor.fetchone()

        summary["top_user"] = (
            user["username"]
            if user
            else "-"
        )

        # Top external or meaningful source IP
        cursor.execute("""
            SELECT
                source_ip,
                COUNT(*) AS total
            FROM logs
            WHERE source_ip IS NOT NULL
              AND source_ip != ''
              AND source_ip NOT IN (
                  'localhost',
                  '127.0.0.1',
                  '::1',
                  'N/A'
              )
            GROUP BY source_ip
            ORDER BY total DESC
            LIMIT 1
        """)

        ip = cursor.fetchone()

        summary["top_ip"] = (
            ip["source_ip"]
            if ip
            else "-"
        )

        return summary

    finally:
        cursor.close()
        connection.close()