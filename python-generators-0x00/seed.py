import mysql.connector
import uuid
import csv


def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mummysdaycjflute",)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    print("Connection successful")


def create_database(connection):
    try:
        connection.cursor().execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.close()
    return connection


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mummysdaycjflute",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    try:
        connection.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS user_data (
                id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age INT NOT NULL
            );
            """
        )
        print("Table user_data created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return connection


def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)  # Reads using column headers
            for row in reader:
                sql = "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)"
                values = (
                    row["name"],
                    row["email"],
                    int(row["age"])
                )
                cursor.execute(sql, values)
        connection.commit()
        print(f"{cursor.rowcount} rows inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return connection


# Create a db connection. 1st connection
ALX_prodev_db = connect_db()

# Create the ALX_prodev database
create_database(ALX_prodev_db)

# Create a connection to the ALX_prodev database 2nd connection
ALX_prodev_db = connect_to_prodev()

# Create the user_data table
create_table(ALX_prodev_db)

# Insert data from a CSV file
insert_data(ALX_prodev_db, "user_data.csv")

# Close the connection
ALX_prodev_db.close()
