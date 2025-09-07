import mysql.connector


def ALX_prodev_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mummysdaycjflute",
        database="ALX_prodev"
    )
    return connection


def stream_users_in_batches(batch_size):
    try:
        connection = ALX_prodev_db()
        cursor = connection.cursor(dictionary=True)
        offset = 0

       # Get total row count
        cursor.execute("SELECT COUNT(*) AS total FROM user_data;")
        total_rows = cursor.fetchone()["total"]

        # Loop through batches
        while offset < total_rows:
            sql = f"SELECT * FROM user_data ORDER BY id LIMIT {batch_size} OFFSET {offset};"
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                yield row

            print("=" * 100)
            offset += batch_size
        else:
            print("No more rows to fetch.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def batch_processing(batch_size):
    # Process batches to filter users over age 25
    for row in stream_users_in_batches(batch_size):
        if row["age"] > 25:
            yield f"ID: {row['id']}, Name: {row['name']}, Email: {row['email']}, Age: {row['age']}"
