import operator

from aiogram_dialog.widgets.kbd import Group, Start, Url, ScrollingGroup, Select, Button, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.common.scroll import sync_scroll
from bot.dialogs.main_menu import states, selected
from bot.utils.i18n_utils.i18n_format import I18nFormat


def main_menu_kb():
    return Group(
        Button(
            Const('Магазин'),
            id='store',
            on_click=selected.on_select_store
        ),
        Button(
            Const("Админ-панель"),
            id='admin_panel',
            on_click=selected.on_select_admin_panel,
            when='is_admin'
        )
    )


def categories_kb(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[1]} [{item[2]}]"),
            id='category',
            items='categories_list',
            on_click=on_click,
            item_id_getter=operator.itemgetter(0)
        ),
        id='categories_list_s_g',
        height=6,
        width=1,
        hide_on_single_page=True
    )


def items_in_category_kb(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id='item',
            items='items_list',
            on_click=on_click,
            item_id_getter=operator.itemgetter(0)
        ),
        id='items_list_s_g',
        height=1,
        width=1,
        hide_on_single_page=True,
        on_page_changed=sync_scroll('text_list')
    )


def currency_kb(on_click):
    return Group(
        Select(
            Format("{item[0]}"),
            id='currency',
            items='currencies',
            on_click=on_click,
            item_id_getter=operator.itemgetter(1)
        ),
        width=1,
    )