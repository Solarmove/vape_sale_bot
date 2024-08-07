from aiogram_dialog import Window
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Multi, Const, List
from aiogram_dialog.widgets.kbd import Cancel, Back, Row, Url
from magic_filter import F

from bot.dialogs.main_menu import states, selected, getters, keyboards


def main_menu_window():
    return Window(
        Const("Главное меню"),
        keyboards.main_menu_kb(),
        state=states.MainMenu.select_action,
        getter=getters.main_menu_getter,
    )


def store_window():
    return Window(
        Const("Выберите категорию"),
        keyboards.categories_kb(selected.on_select_category),
        Cancel(Const("Назад")),
        state=states.Store.select_category,
        getter=getters.category_getter,
    )


def items_in_category_window():
    return Window(
        Multi(
            Const("Выберите товар"),
            List(
                Format(
                    "<b>{item[1]}</b>\n\nЦена: <code>{item[2]} USD</code>\n\n"
                    "<i>{item[3]}</i>"
                ),
                id="text_list",
                items="items_list",
                page_size=1,
            ),
            sep="\n\n",
        ),
        DynamicMedia(selector="current_photo"),
        keyboards.items_in_category_kb(selected.on_select_item),
        Row(Back(Const("Назад")), Cancel(Const("Закрыть"))),
        state=states.Store.select_item,
        getter=getters.items_in_category_getter,
    )


def select_currency_window():
    return Window(
        Const("Выберите валюту"),
        keyboards.currency_kb(selected.on_select_currency),
        Cancel(Const("Назад")),
        state=states.Purchase.select_currency,
        getter=getters.currency_getter,
    )


def create_invoice_window():
    return Window(
        Const("Создание счета"),
        Format(
            "Счет на сумму <b>{total_price}</b> успешно создан.\n\n"
            "Номер транзакции в боте: <code>{invoice_id}</code>\n\n"
            "<i>Сума автоматически конвертируеца в выбраную вами валюту</i>"
        ),
        Url(Const("Оплатить"), Format("{url}")),
        Back(Const("Закрыть")),
        state=states.Purchase.create_invoice,
        getter=getters.invoice_getter,
    )
