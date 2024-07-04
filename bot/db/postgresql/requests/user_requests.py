import datetime

from sqlalchemy import select, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bot.db.postgresql.model.models import *


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int):
        stmt = (
            select(User)
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    