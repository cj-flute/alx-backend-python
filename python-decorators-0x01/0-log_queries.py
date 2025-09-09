import sqlite3
import functools


"""
    import sqlite3
    cx = sqlite3.connect("test.db")  # test.db will be created or opened
    The special path name ":memory:" can be provided to connect to a transient in-memory database:

    cx = sqlite3.connect(":memory:")  # connect to a database in RAM
    Once a connection has been established, create a Cursor object and call its execute() method to perform SQL queries:

    cu = cx.cursor()

      # create a table
    cu.execute("create table lang(name, first_appeared)")

    # insert values into a table
    cu.execute("insert into lang values (?, ?)", ("C", 1972))

    # execute a query and iterate over the result
    for row in cu.execute("select * from lang"):
        print(row)

    cx.close()
"""

# decorator to lof SQL queries

""" YOUR CODE GOES HERE"""


def log_queries(func):
    def wrapper(query):
        query = ("SET GLOBAL general_log = 'on';")
        func(query)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
