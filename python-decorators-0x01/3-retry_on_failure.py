import time
import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def retry_on_failure(retries, delay):
    def decorator(func):
        @function.wrap(func)
        def wrapper(*args, **kwargs):
            try:
                if (retries > 0 and delay > 0):
                    return func(*args, **kwargs)
            except sqlite3.Error as err:
                print(f"Database Error: {err}. Retrying in {delay} seconds...")
                time.sleep(delay)
                return wrapper(retries - 1, delay)
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# attempt to fetch users with automatic retry on failure


users = fetch_users_with_retry()
print(users)
