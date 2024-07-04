import datetime

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from configreader import config

