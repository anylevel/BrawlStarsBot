import aiosqlite


async def create_table() -> None:
    async with aiosqlite.connect("stats.db") as db:
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS users (id integer primary key , user_name text , game_hashtag text)''')
        await db.commit()

