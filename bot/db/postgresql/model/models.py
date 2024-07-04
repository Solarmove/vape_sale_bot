from sqlalchemy import (
    ForeignKey,
    VARCHAR,
    BIGINT,
    TEXT, INTEGER, UniqueConstraint, func, BOOLEAN,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from bot.db.postgresql.base import Base


class User(Base):
    __tablename__ = "user"

    id = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username = mapped_column(VARCHAR(255), nullable=True)
    full_name = mapped_column(VARCHAR(255), nullable=False)
    transactions: Mapped[list['Transactions']] = Relationship(back_populates='user')
   

class Category(Base):
    __tablename__ = "category"

    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name = mapped_column(VARCHAR(255), nullable=False)
    items: Mapped[list['Item']] = Relationship(back_populates='category')


class Item(Base):
    __tablename__ = "item"

    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name = mapped_column(VARCHAR(255), nullable=False)
    description = mapped_column(TEXT, nullable=False)
    price = mapped_column(INTEGER, nullable=False)
    file_id = mapped_column(VARCHAR(255), nullable=False)
    file_unique_id = mapped_column(VARCHAR(255), nullable=False)
    category_id = mapped_column(BIGINT, ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category: Mapped['Category'] = Relationship(back_populates='items')


class Transactions(Base):
    __tablename__ = "transactions"

    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id = mapped_column(BIGINT, ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = Relationship(back_populates='transactions')
    item_id = mapped_column(BIGINT, ForeignKey('item.id'), nullable=False)
    item: Mapped['Item'] = Relationship(back_populates='transactions')
    status = mapped_column(BOOLEAN, nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False, default=func.now())

