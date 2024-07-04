import datetime

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from configreader import config


async def category_edit_param_list_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):
    return {
        "category_param_list": [
            ("name", "Название"),
            ('delete', 'Удалить категорию')
            ]
        }


async def new_item_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):
    return {
        'name': dialog_manager.dialog_data.get('name'),
        'desc': dialog_manager.dialog_data.get('description'),
        'price': dialog_manager.dialog_data.get('price'),
        'photo': MediaAttachment(
            file_id=MediaId(
                file_id=dialog_manager.dialog_data.get('photo_id'), # type: ignore
                file_unique_id=dialog_manager.dialog_data.get('photo_unique_id')
            ),
            type=ContentType.PHOTO
        )

    }


async def item_edit_param_list_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):
    return {
        "item_param_list": [
            ("name", "Название"),
            ("description", "Описание"),
            ("price", "Цена"),
            ("photo", "Фото"),
            ('category', 'Категория'),
            ('delete', 'Удалить товар')
            ]
        }