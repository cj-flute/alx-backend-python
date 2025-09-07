import mysql.connector


def ALX_prodev_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mummysdaycjflute",
        database="ALX_prodev"
    )
    return connection


def paginate_users(page_size, offset):
    # Fetch a page of users from the DB
    try:
        connection = ALX_prodev_db()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
        return rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def lazy_paginate(page_size):
    # Generator to lazily fetch users page by page
    try:
        connection = ALX_prodev_db()
        cursor = connection.cursor(dictionary=True)
        offset = 0
        while True:
            rows = paginate_users(page_size, offset)
            if not rows:  # no more data
                break
            for row in rows:
                yield row  # yield each user lazily
            offset += page_size

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


for user in lazy_paginate(10):
    print(user)
