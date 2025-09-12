# Run multiple database queries concurrently using asyncio.gather.
import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as conn:
        async with conn.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    all_users, older_users = results
    print("All Users:", all_users)
    print("Older Users:", older_users)


asyncio.run(fetch_concurrently())
