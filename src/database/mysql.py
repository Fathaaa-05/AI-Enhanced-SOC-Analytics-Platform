import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="100105",
        database="soc_ai_platform"
    )

    return connection