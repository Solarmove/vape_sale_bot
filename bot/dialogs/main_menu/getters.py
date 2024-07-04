from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import User
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from bot.services.qr_service import create_qr_code

