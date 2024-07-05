# -*- coding: utf-8 -*-
import asyncio
import os
from aiohttp import web
from aiogram import F, Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import (
    RedisEventIsolation,
    RedisStorage,
)
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from aiogram_i18n.cores import FluentRuntimeCore
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from bot.db.postgresql.base import Base
from bot.db.redis import redis
from bot.dialogs import dialogs_list
from bot.handlers import routers_list
from bot.handlers.webhooks import handle_np_webhook
from bot.middlewares.devs_protect import DevsProtectMiddleware
from bot.middlewares.i18n_dialog import RedisI18nMiddleware
from bot.services.startup_actions import add_default_objects
from bot.utils.i18n_utils.i18n_format import make_i18n_middleware
from bot.utils.logging import logger
from bot.utils.set_bot_commands import set_default_commands
from configreader import config
from .middlewares.db import DbSessionMiddleware


async def main():
    engine = create_async_engine(str(config.postgredsn), future=True, echo=False)

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # Creating DB connections pool
    db_pool = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    await add_default_objects(db_pool)

    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode="HTML", show_caption_above_media=True))
    key_builder = DefaultKeyBuilder(with_destiny=True, with_bot_id=True)
    storage = RedisStorage(redis=redis, key_builder=key_builder)
    event_isolation = RedisEventIsolation(redis, key_builder=key_builder)

    dp = Dispatcher(storage=storage, events_isolation=event_isolation)

    router = Router(name=__name__)

    LOCALES = ["ru"]
    path_to_locales = os.path.join("bot", "locales", "{locale}", "LC_MESSAGES")
    i18n_middleware = RedisI18nMiddleware(
        core=FluentRuntimeCore(path=path_to_locales),
        default_locale="ru",
        redis=redis,
        locales_list=LOCALES,
    )
    i18n_dialog_middleware = make_i18n_middleware(path_to_locales, LOCALES)

    # dp.startup.register(on_startup)
    dp["dp"] = dp
    dp["session_pool"] = db_pool

    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type == "private")
    dp.update.middleware(i18n_dialog_middleware)
    dp.update.middleware(DbSessionMiddleware(db_pool))
    # if config.bot_mode == "dev":
    #     dp.update.middleware(DevsProtectMiddleware())
    #     dp.update.outer_middleware(DevsProtectMiddleware())

    # Router including
    router.include_routers(*routers_list)
    router.include_routers(*dialogs_list)
    dialog_manager_bg_factory = setup_dialogs(dp)
    dp.include_router(router)

    app = web.Application()
    app['session_factory'] = db_pool
    app['bg_factory'] = dialog_manager_bg_factory
    app['bot'] = bot
    app.router.add_post(config.webhook_path, handle_np_webhook)

    i18n_middleware.setup(dispatcher=dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_default_commands(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner, host=config.webhook_host, port=config.webhook_port
    )
    await site.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
