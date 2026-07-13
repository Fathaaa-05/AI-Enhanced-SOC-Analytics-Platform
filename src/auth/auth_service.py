from werkzeug.security import check_password_hash

from src.database.mysql import get_connection


def authenticate_user(username, password):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT username, password, role
            FROM users
            WHERE username = %s
            LIMIT 1
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return {"success": False}

        if not check_password_hash(user["password"], password):
            return {"success": False}

        return {
            "success": True,
            "username": user["username"],
            "role": user["role"]
        }

    finally:
        cursor.close()
        connection.close()