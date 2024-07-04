import random
import string

from bot.db.postgresql import Repo



async def add_default_objects(db_factory):
    async with db_factory() as session:
        repo = Repo(session=session)
        