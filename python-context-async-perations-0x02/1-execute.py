# A reusable context manager that takes a query as input and executes it, managing both connection and the query execution
class ExecuteQuery:
    def __init__(self, db_name, query, parameters=None):
        self.db_name = db_name
        self.conn = None
        self.query = None
        self.parameters = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        import sqlite3
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(self.query, self.parameters)
            self.results = self.cursor.fetchall()
            return self.results
        except Exception as e:
            print(f"An error occurred during query execution: {e}")
            self.conn.rollback()
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"An error occurred: {exc_value}")
            self.conn.rollback()

        if self.conn:
            self.conn.close()


with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(f"Query Results: {results}")
