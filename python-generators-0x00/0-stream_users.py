# A generator function that streams rows from an SQL database one by one.

import mysql.connector


def stream_users():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="mummysdaycjflute",
            database="ALX_prodev"
        )
        my_cursor = connection.cursor(dictionary=True)
        my_cursor.execute("SELECT * FROM user_data;")
        for row in my_cursor:
            yield row
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            my_cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Example usage:
# for user in stream_users():
#     print(user)
# Note: Ensure that the MySQL server is running and the database/table exists.
