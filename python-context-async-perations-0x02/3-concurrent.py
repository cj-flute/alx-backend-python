# Run multiple database queries concurrently using asyncio.gather.
import asyncio
import aiosqlite


async def async_fetch_users(connection):
    cursor = await connection.cursor()
    await cursor.execute("SELECT * FROM users")
    users = await cursor.fetchall()
    await cursor.close()
    return users


async def async_fetch_older_users(connection):
    cursor = await connection.cursor()
    await cursor.execute("SELECT * FROM older_users")
    older_users = await cursor.fetchall()
    await cursor.close()
    return older_users


async def main():
    async with aiosqlite.connect('users.db') as conn:
        tasks = [
            async_fetch_users(conn),
            async_fetch_older_users(conn)
        ]
        results = await asyncio.gather(*tasks)
        all_users, older_users = results
        print("All Users:", all_users)
        print("Older Users:", older_users)

asyncio.run(main())
