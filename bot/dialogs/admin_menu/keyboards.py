import operator

from aiogram_dialog.widgets.kbd import Group, Start, Url, ScrollingGroup, Select, Button, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.admin_menu import states, selected
from bot.utils.i18n_utils.i18n_format import I18nFormat


def admin_menu_kb():
    return Group(
        Button(
            Const('Настройки категорий'),
            id='settings_categories',
            on_click=selected.on_select_settings_categories
        ),
        Button(
            Const('Настройки товаров'),
            id='settings_items',
            on_click=selected.on_select_settings_items
        ),
    )



def edit_category_kb(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id='category_param',
            items='category_param_list',
            on_click=on_click,
            item_id_getter=operator.itemgetter(0)
        ),
        id='categories_list_s_g',
        height=6,
        width=1,
        hide_on_single_page=True
    )


def edit_item_kb(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id='item_param',
            items='item_param_list',
            on_click=on_click,
            item_id_getter=operator.itemgetter(0)
        ),
        id='items_list_s_g',
        height=6,
        width=1,
        hide_on_single_page=True
    )