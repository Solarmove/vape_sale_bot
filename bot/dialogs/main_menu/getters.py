import logging
from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import User
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common.scroll import ManagedScroll
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_i18n import I18nContext
from bot.db.postgresql.model.models import Transactions
from bot.services.now_payments import (
    CreateInvoiceData,
    CreatedInvoiceResult,
    NowPayments,
)
from configreader import config

from bot.db.postgresql import Repo


async def main_menu_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):
    print(event_from_user.id, config.admins)
    # event_from_user.id in config.admins
    return {"is_admin": True}


async def category_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):

    categories_list = dialog_manager.dialog_data.get("categories_list", [])
    if not categories_list:
        categories_model = await repo.user_repo.get_categories()
        for category in categories_model:
            items_in_category_count = await repo.user_repo.get_items_count_in_category(
                category.id
            )
            categories_list.append(
                (category.id, category.name, items_in_category_count)
            )
        dialog_manager.dialog_data.update(categories_list=categories_list)
    return {"categories_list": categories_list}


async def items_in_category_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):
    category_id = dialog_manager.dialog_data.get("category_id")
    scroll: ManagedScroll | None = dialog_manager.find("items_list_s_g")
    if scroll is None:
        raise ValueError("scroll items_list_s_g is None")
    if category_id is None:
        raise ValueError("category_id is None")

    current_page = await scroll.get_page()
    items_list = dialog_manager.dialog_data.get("items_list", [])
    media_list = dialog_manager.dialog_data.get("media_list", [])
    if not items_list or not media_list:
        items_model = await repo.user_repo.get_items_by_category(category_id)
        for item in items_model:
            items_list.append((item.id, item.name, item.price, item.description))
            media_list.append(
                MediaAttachment(
                    file_id=MediaId(
                        file_id=item.file_id,
                        file_unique_id=item.file_unique_id,
                    ),
                    type=ContentType.PHOTO,
                )
            )
        # dialog_manager.dialog_data.update(items_list=items_list, media_list=media_list)
    try:
        current_page_photo = media_list[current_page]
    except IndexError:
        current_page_photo = None
    return {
        "items_list": items_list,
        "media_list": media_list,
        "current_photo": current_page_photo,
    }


async def currency_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):
    return {
        "currencies": [
            ("LTC", "ltc"),
            ("USDT(TRC20)", "usdttrc20"),
            ("TRX", "trx"),
            ("BTC", "btc"),
        ]
    }


async def invoice_getter(
    dialog_manager: DialogManager, event_from_user: User, bot: Bot, repo: Repo, **kwargs
):
    item_model: Item = await repo.user_repo.get_item(dialog_manager.start_data.get("item_id"))  # type: ignore
    transaction = Transactions(
        item_id=item_model.id,
        user_id=event_from_user.id,
        status=False,
    )
    transaction = await repo.add_one(transaction, commit=False)
    invoice_data = CreateInvoiceData(
        price_amount=item_model.price,
        price_currency="USD",
        pay_currency=dialog_manager.dialog_data.get("currency"),
        order_id=str(transaction.id),
        order_description=item_model.name,
        ipn_callback_url=config.base_url,  # type: ignore
        # success_url=config.success_url,
        # cancel_url=config.cancel_url,
    )

    try:
        now_pay = NowPayments(
            api_key=config.x_api_key,
            ipn_key=config.ipn_callback,
        )
        response: CreatedInvoiceResult = await now_pay.create_invoice(invoice_data)
    except Exception as e:
        logging.error(f"Error while creating invoice: {e}")
        await repo.session.rollback()
        raise e
    await repo.session.commit()
    return {
        "total_price": item_model.price,
        "currency": "USD",
        "invoice_id": response.order_id,
        "url": response.invoice_url,
    }
