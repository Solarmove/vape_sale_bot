import datetime
import logging
from operator import attrgetter

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from bot.db.postgresql.model.models import User
from bot.dialogs.admin_menu import states
from bot.dialogs.main_menu.states import EnterPromocode


