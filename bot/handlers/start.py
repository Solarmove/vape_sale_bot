from aiogram import Bot
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from bot.db.postgresql.model.models import User
from configreader import config

router = Router()


@router.message(CommandStart())
async def start(
        message: Message,
        command: CommandObject,
        repo: Repo,
        bot: Bot,
        dialog_manager: DialogManager,
        i18n: I18nContext,
):
    ...
