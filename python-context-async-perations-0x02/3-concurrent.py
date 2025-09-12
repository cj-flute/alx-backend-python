# Run multiple database queries concurrently using asyncio.gather.
import asyncio
import aiosqlite


async def async_fetch_users(connection):
    async with connection.execute("SELECT * FROM users") as cursor:
        return await cursor.fetchall()


async def async_fetch_older_users(connection):
    async with connection.execute("SELECT * FROM users WHERE age > 40") as cursor:
        return await cursor.fetchall()


async def fetch_concurrently():
    async with aiosqlite.connect('users.db') as conn:
        all_users, older_users = await asyncio.gather(
            async_fetch_users(conn),
            async_fetch_older_users(conn)
        )
        print("All Users:", all_users)
        print("Older Users:", older_users)


asyncio.run(fetch_concurrently())
