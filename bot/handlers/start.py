from aiogram import Bot
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_i18n import I18nContext

from bot.db.postgresql import Repo
from bot.db.postgresql.model.models import User
from bot.dialogs.main_menu.states import MainMenu
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
    if not message.from_user:
        return
    user_exists = await repo.user_repo.get_user(message.from_user.id)
    if not user_exists:
        user = User(
            id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
        )
        await repo.add_one(user)
    await dialog_manager.start(state=MainMenu.select_action, mode=StartMode.RESET_STACK)
