from aiogram import Bot
from aiogram_dialog import BgManagerFactory
from aiohttp import web
import json
from pprint import pprint

from bot.db.postgresql import Repo


async def handle_np_webhook(request: web.Request):
    # Получение данных из POST-запроса
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON"}, status=400)
    if data.get("payment_status") in ["finished", "confirming"]:
        payment_status = data["payment_status"]
        order_id = int(data["order_id"])
        session_factory = request.app["session_factory"]
        bg_factory: BgManagerFactory = request.app["bg_factory"]
        bot: Bot = request.app["bot"]
        async with session_factory() as session:
            repo = Repo(session)
            transaction = await repo.user_repo.get_transaction_by_id(order_id)
            if transaction:
                if payment_status == "finished":
                    await bot.send_message(
                        transaction.user_id,
                        f"Ваш заказ #{transaction.id} успешно оплачен!\n\nМы свяжемся с вами в ближайшее время для уточнения деталей.",
                    )
                    text_for_admins = (
                        "Поступил новый заказ!\n\n"
                        f"ID заказа: {transaction.id}\n"
                        f"Пользователь: {transaction.user.full_name} {transaction.user.username}\n"
                        f"Товар: {transaction.item.name} {transaction.item.price}\n"
                    )
                    await repo.user_repo.update_transaction(transaction.id, status=True)
                else:
                    await bg_factory.bg(
                        bot=bot,
                        chat_id=transaction.user_id,
                        user_id=transaction.user_id,
                    ).done()
                    await bot.send_message(
                        transaction.user_id,
                        f"Ваш заказ #{transaction.id} находится в процессе оплаты. Пожалуйста, дождитесь подтверждения.",
                    )

    response_data = {
        "status": "success",
        "message": "Webhook received successfully",
        "received_data": data,
    }

    return web.json_response(response_data)
