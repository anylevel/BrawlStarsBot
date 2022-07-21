import aiosqlite
from tortoise import Tortoise


async def create_table() -> None:
    async with aiosqlite.connect("stats.db"):
        pass


async def init():
    await Tortoise.init(
        db_url="sqlite://stats.db",
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
