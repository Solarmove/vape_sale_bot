import logging
from typing import Sequence

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from bot.db.postgresql.model.models import User, LevelPrise, Cocktail
from bot.dialogs.main_menu import states
