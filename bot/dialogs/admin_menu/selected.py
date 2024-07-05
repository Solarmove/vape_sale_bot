import datetime
import logging
from operator import attrgetter

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button

from bot.db.postgresql import Repo
from bot.db.postgresql.model.models import Category, Item, User
from bot.dialogs.admin_menu import states


async def on_select_settings_categories(
    call: CallbackQuery, widget: Button, manager: DialogManager
):
    await manager.start(states.EditCategory.select_category)


async def on_select_settings_items(
    call: CallbackQuery, widget: Button, manager: DialogManager
):
    await manager.start(states.EditItem.select_category)


async def on_add_category(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(states.CreateCategory.enter_name)


async def on_select_category_for_edit(
    call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    try:
        item_id = int(item_id)  # type: ignore
    except ValueError:
        logging.error(f"item_id is not integer: {item_id}")
        return

    manager.dialog_data.update(category_id=item_id)
    await manager.switch_to(states.EditCategory.select_edit_param)


async def on_select_edit_category_param(
    call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    edit_params_mapping = {
        "name": states.ChangeCategoryName.enter_new_name,
        "delete": states.DeleteCategory.confirm,
    }
    await manager.start(edit_params_mapping[item_id], data=manager.dialog_data)


async def on_change_category_name(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_name = message_text[:100]
    category_id = manager.start_data["category_id"]
    repo: Repo = manager.middleware_data["repo"]
    try:
        await repo.user_repo.update_category(category_id, name=new_name)
    except Exception:
        await message.answer(f"Ошибка при изменении названия категории")
        return await manager.done()
    await message.answer(f"Название категории изменено на <b>{new_name}</b>")
    await manager.done()


async def on_send_new_category(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_name = message_text
    repo: Repo = manager.middleware_data["repo"]
    category_exist = await repo.user_repo.get_category_by_name(new_name)
    if category_exist:
        await message.answer(f"Категория с таким названием уже существует")
        return await manager.done()
    try:
        new_category_model = Category(name=new_name)
        await repo.add_one(new_category_model)
    except Exception:
        await message.answer(f"Ошибка при создании категории")
        return await manager.done()
    await message.answer(f"Категория <b>{new_name}</b> создана")
    await manager.done()


async def on_confirm_delete_category(
    call: CallbackQuery, widget: Button, manager: DialogManager
):
    category_id = manager.start_data["category_id"]
    repo: Repo = manager.middleware_data["repo"]
    try:
        await repo.user_repo.delete_category(category_id)
    except Exception:
        await call.answer(f"Ошибка при удалении категории", show_alert=True)
        return await manager.done()

    await call.answer(f"Категория удалена", show_alert=True)
    return await manager.done()


async def on_select_catgory_for_edit_item(
    call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    try:
        item_id = int(item_id)  # type: ignore
    except ValueError:
        logging.error(f"item_id is not integer: {item_id}")
        return

    manager.dialog_data.update(category_id=item_id)
    await manager.switch_to(states.EditItem.select_item)


async def on_start_add_item(
    call: CallbackQuery, widget: Button, manager: DialogManager
):
    await manager.start(states.CreateItem.enter_name, data=manager.dialog_data)


async def on_select_item_for_edit(
    call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    try:
        item_id = int(item_id)  # type: ignore
    except ValueError:
        logging.error(f"item_id is not integer: {item_id}")
        return

    manager.dialog_data.update(item_id=item_id)
    await manager.switch_to(states.EditItem.select_edit_param)


async def on_enter_new_item_name(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_name = message_text[:100]
    repo: Repo = manager.middleware_data["repo"]
    manager.dialog_data.update(name=new_name)
    await manager.switch_to(states.CreateItem.enter_price)


async def on_enter_new_item_price(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_price = message_text
    try:
        new_price = float(new_price)
    except ValueError:
        await message.answer(f"Цена должна быть числом")
        return await manager.done()
    manager.dialog_data.update(price=new_price)
    await manager.switch_to(states.CreateItem.enter_description)


async def on_enter_new_item_description(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_description = message_text
    manager.dialog_data.update(description=new_description[:500])
    await manager.switch_to(states.CreateItem.send_photo)


async def on_send_photo_for_new_item(
    message: Message, widget: MessageInput, manager: DialogManager
):
    if message and message.photo:
        manager.dialog_data.update(
            photo_id=message.photo[-1].file_id,
            photo_unique_id=message.photo[-1].file_unique_id,
        )
    else:
        await message.answer("Отправьте фото")
        return
    await manager.switch_to(states.CreateItem.confirm)


async def on_save_new_item(call: CallbackQuery, widget: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data["repo"]
    category_id = manager.start_data["category_id"]
    name = manager.dialog_data["name"]
    price = manager.dialog_data["price"]
    description = manager.dialog_data["description"]
    photo_id = manager.dialog_data["photo_id"]
    photo_unique_id = manager.dialog_data["photo_unique_id"]
    new_item_model = Item(
        name=name,
        description=description,
        price=price,
        file_id=photo_id,
        file_unique_id=photo_unique_id,
        category_id=category_id,
    )
    try:
        await repo.add_one(new_item_model)
    except Exception as ex:
        await call.answer(
            f"Ошибка при добавлении товара. Попытайтесь самостоятельно исправить ошибку: {ex}",
            show_alert=True,
        )
        return
    await call.answer(f"Товар {name} добавлен", show_alert=True)
    await manager.done()


async def on_select_edit_param(
    call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    edit_params_mapping = {
        "name": states.EditItemName.enter_new_name,
        "description": states.EditItemDescription.enter_new_description,
        "price": states.EditItemPrice.enter_new_price,
        "photo": states.EditItemPhoto.send_new_photo,
        "category": states.EditItemCategory.select_new_category,
        "delete": states.DeleteItem.confirm,
    }
    await manager.start(edit_params_mapping[item_id], data=manager.dialog_data)


async def on_change_item_name(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_name = message_text[:100]
    item_id = manager.start_data["item_id"]
    repo: Repo = manager.middleware_data["repo"]
    try:
        await repo.user_repo.update_item(item_id, name=new_name)
    except Exception:
        await message.answer(f"Ошибка при изменении названия товара")
        return await manager.done()
    await message.answer(f"Название товара изменено на <b>{new_name}</b>")
    await manager.done()


async def on_change_item_price(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_price = message_text
    try:
        new_price = float(new_price)
    except ValueError:
        await message.answer(f"Цена должна быть числом")
        return await manager.done()
    item_id = manager.start_data["item_id"]
    repo: Repo = manager.middleware_data["repo"]
    try:
        await repo.user_repo.update_item(item_id, price=new_price)
    except Exception:
        await message.answer(f"Ошибка при изменении цены товара")
        return await manager.done()
    await message.answer(f"Цена товара изменена на <b>{new_price}</b>")
    await manager.done()


async def on_change_item_description(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    new_description = message_text
    item_id = manager.start_data["item_id"]
    repo: Repo = manager.middleware_data["repo"]
    try:
        await repo.user_repo.update_item(item_id, description=new_description[:500])
    except Exception:
        await message.answer(f"Ошибка при изменении описания товара")
        return await manager.done()
    await message.answer(f"Описание товара изменено")
    await manager.done()


async def on_send_new_photo_for_item(
    message: Message, widget: MessageInput, manager: DialogManager
):
    if message and message.photo:
        repo: Repo = manager.middleware_data["repo"]
        item_id = manager.start_data["item_id"]
        photo_id = message.photo[-1].file_id
        photo_unique_id = message.photo[-1].file_unique_id
        try:
            await repo.user_repo.update_item(
                item_id, file_id=photo_id, file_unique_id=photo_unique_id
            )
        except Exception:
            await message.answer(f"Ошибка при изменении фото товара")
            return await manager.done()
    else:
        await message.answer("Отправьте фото")
        return


async def on_confirm_delete_item(
    call: CallbackQuery, widget: Button, manager: DialogManager
):
    item_id = manager.dialog_data["item_id"]
    repo: Repo = manager.middleware_data["repo"]
    try:
        await repo.user_repo.delete_item(item_id)
    except Exception:
        await call.answer(f"Ошибка при удалении товара", show_alert=True)
        return await manager.done()

    await call.answer(f"Товар удален", show_alert=True)
    return await manager.done()


async def on_select_new_item_category(
    call: CallbackQuery, widget: Select, manager: DialogManager, category_id: str
):
    try:
        category_id = int(category_id)  # type: ignore
    except ValueError:
        logging.error(f"category_id is not integer: {category_id}")

    item_id = manager.start_data["item_id"]
    repo: Repo = manager.middleware_data["repo"]
    try:
        await repo.user_repo.update_item(item_id, category_id=category_id)
    except Exception:
        await call.answer(f"Ошибка при изменении категории товара", show_alert=True)
        return await manager.done()
    await call.answer(f"Категория товара изменена", show_alert=True)
    await manager.done()
