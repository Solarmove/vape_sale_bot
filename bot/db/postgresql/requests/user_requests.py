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

    async def get_users(self):
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_categories(self):
        stmt = select(Category)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_category(self, category_id: int):
        stmt = (
            select(Category)
            .where(Category.id == category_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_category_by_name(self, name: str):
        stmt = (
            select(Category)
            .where(Category.name == name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_items_count_in_category(self, category_id: int):
        stmt = (
            select(func.count(Item.id))
            .where(Item.category_id == category_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def delete_category(self, category_id: int):
        stmt = (
            delete(Category)
            .where(Category.id == category_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_items(self):
        stmt = select(Item)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_item(self, item_id: int):
        stmt = (
            select(Item)
            .where(Item.id == item_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_items_by_category(self, category_id: int):
        stmt = (
            select(Item)
            .where(Item.category_id == category_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def delete_item(self, item_id: int):
        stmt = (
            delete(Item)
            .where(Item.id == item_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_all_items_in_category(self, category_id: int):
        stmt = (
            delete(Item)
            .where(Item.category_id == category_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_all_items(self):
        stmt = delete(Item)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_item_by_name(self, name: str):
        stmt = (
            select(Item)
            .where(Item.name == name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def update_item(self, item_id: int, **kwargs):
        stmt = (
            update(Item)
            .where(Item.id == item_id)
            .values(**kwargs)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_category(self, category_id: int, **kwargs):
        stmt = (
            update(Category)
            .where(Category.id == category_id)
            .values(**kwargs)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_transaction_by_id(self, transaction_id: int):
        stmt = (
            select(Transactions)
            .where(Transactions.id == transaction_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_transactions(self):
        stmt = select(Transactions)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_transactions_by_user(self, user_id: int):
        stmt = (
            select(Transactions)
            .where(Transactions.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_transactions_by_item(self, item_id: int):
        stmt = (
            select(Transactions)
            .where(Transactions.item_id == item_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_transaction_by_category(self, category_id: int):
        stmt = (
            select(Transactions)
            .join(Item)
            .where(Item.category_id == category_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()