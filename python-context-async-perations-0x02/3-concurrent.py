# Run multiple database queries concurrently using asyncio.gather.
import asyncio
import aiosqlite


async def async_fetch_users(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users")
        users = await cursor.fetchall()
    return users


async def async_fetch_older_users(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM older_users WHERE age > 40")
        older_users = await cursor.fetchall()
        await cursor.close()
    return older_users


async def fetch_concurrently():
    async with aiosqlite.connect('users.db') as conn:
        results = await asyncio.gather(
            async_fetch_users(conn),
            async_fetch_older_users(conn)
        )
        all_users, older_users = results
        print("All Users:", all_users)
        print("Older Users:", older_users)

asyncio.run(fetch_concurrently())
