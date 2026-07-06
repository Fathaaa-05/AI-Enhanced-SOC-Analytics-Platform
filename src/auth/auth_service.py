from src.database.mysql import get_connection


def authenticate_user(username, password):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT username, role
    FROM users
    WHERE username=%s AND password=%s
    """

    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return {
            "success": True,
            "username": user["username"],
            "role": user["role"]
        }

    return {
        "success": False
    }