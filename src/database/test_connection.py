from src.database.mysql import get_connection

try:
    connection = get_connection()

    if connection.is_connected():
        print("✅ Connected to MySQL Successfully!")

    connection.close()

except Exception as e:
    print("Connection Error:", e)