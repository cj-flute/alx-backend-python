import mysql.connector


def ALX_prodev_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mummysdaycjflute",
        database="ALX_prodev"
    )
    return connection


def stream_user_ages():
    try:
        connection = ALX_prodev_db()
        cursor = connection.cursor(dictionary=True)

        sql = f"SELECT age FROM  user_data;"
        cursor.execute(sql)

        for age_row in cursor:
            yield age_row['age']

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL Connection is closed")


def user_average_age():
    # Compute average age without loading all data into memory
    ages = 0
    total_users = 0

    age_rows = stream_user_ages()

    for row in age_rows:
        ages += row
        total_users += 1
        average = ages / total_users

    print(f"Average age of users: {average}")
