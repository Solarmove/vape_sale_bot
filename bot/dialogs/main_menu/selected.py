import logging
from typing import Sequence

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from bot.db.postgresql.model.models import User
from bot.dialogs.main_menu import states


async def on_select_store(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(states.Store.select_category)


async def on_select_category(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    try:
        item_id = int(item_id)  # type: ignore
    except ValueError:
        logging.error(f"item_id is not integer: {item_id}")
        return
    
    manager.dialog_data.update(category_id=item_id)
    await manager.switch_to(states.Store.select_item)


async def on_select_item(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    try:
        item_id = int(item_id)  # type: ignore
    except ValueError:
        logging.error(f"item_id is not integer: {item_id}")
        return
    
    manager.dialog_data.update(item_id=item_id)
    await manager.start(states.Purchase.select_currency, data=manager.dialog_data)


async def on_select_currency(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    manager.dialog_data.update(currency=item_id)
    await manager.switch_to(states.Purchase.create_invoice)
