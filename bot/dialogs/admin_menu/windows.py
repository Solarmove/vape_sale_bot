import operator
from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Select, Back, Calendar
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const, Multi, List

from bot.dialogs.admin_menu import states, selected, getters, keyboards
from bot.dialogs.main_menu.getters import category_getter, items_in_category_getter
from bot.dialogs.main_menu.keyboards import categories_kb, items_in_category_kb


def admin_menu_window():
    return Window(
        Const("Админ меню"),
        keyboards.admin_menu_kb(),
        state=states.AdminMenu.select_action,
    )


def edit_category_window():
    return Window(
        Const("Выберите категорию"),
        Button(
            Const("Добавить категорию"),
            id="add_category",
            on_click=selected.on_add_category,
        ),
        categories_kb(selected.on_select_category_for_edit),
        Cancel(Const("Назад")),
        state=states.EditCategory.select_category,
        getter=category_getter,
    )


def add_category_window():
    return Window(
        Const("Введите название новой категории"),
        TextInput(id="category_name", on_success=selected.on_send_new_category),
        Cancel(Const("Отмена")),
        state=states.CreateCategory.enter_name,
    )


def select_edit_category_param_window():
    return Window(
        Const("Выберите параметр для редактирования"),
        keyboards.edit_category_kb(selected.on_select_edit_category_param),
        Back(Const("Назад")),
        state=states.EditCategory.select_edit_param,
        getter=getters.category_edit_param_list_getter,
    )


def change_category_name_window():
    return Window(
        Const("Введите новое имя категории"),
        TextInput(id="new_name", on_success=selected.on_change_category_name),
        Cancel(Const("Отмена")),
        state=states.ChangeCategoryName.enter_new_name,
    )


def delete_category_window():
    return Window(
        Const("Вы уверены, что хотите удалить категорию?"),
        Button(
            Const("Да"),
            id="delete_category",
            on_click=selected.on_confirm_delete_category,
        ),
        Cancel(Const("Нет")),
        state=states.DeleteCategory.confirm,
    )


def edit_item_window():
    return Window(
        Const("Выберите категорию товара"),
        categories_kb(selected.on_select_catgory_for_edit_item),
        Cancel(Const("Назад")),
        state=states.EditItem.select_category,
        getter=category_getter,
    )


def select_item_for_edit_window():
    return Window(
        Multi(
            Const("Выберите товар для редактирования"),
            List(
                Format(
                    "<b>{item[1]}</b>\n\nЦена: <code>{item[2]} UAH</code>\n\n"
                    "<i>{item[3]}<"
                ),
                id="text_list",
                items="items_list",
            ),
            sep="\n\n",
        ),
        DynamicMedia(selector="current_photo"),
        Button(
            Const("Добавить товар"),
            id='add_item',
            on_click=selected.on_start_add_item,
        ),
        items_in_category_kb(selected.on_select_item_for_edit),
        state=states.EditItem.select_item,
        getter=items_in_category_getter,
    )


def enter_new_item_name_window():
    return Window(
        Const("Введите название товара"),
        TextInput(id="item_name", on_success=selected.on_enter_new_item_name),
        Cancel(Const("Отмена")),
        state=states.CreateItem.enter_name,
    )


def enter_new_item_price_window():
    return Window(
        Const("Введите цену товара"),
        TextInput(id="item_price", on_success=selected.on_enter_new_item_price),
        Back(Const("Назад")),
        state=states.CreateItem.enter_price,
    )


def enter_new_item_description_window():
    return Window(
        Const("Введите описание товара (до 500 символов)"),
        TextInput(id="item_description", on_success=selected.on_enter_new_item_description),
        Back(Const("Назад")),
        state=states.CreateItem.enter_description,
    )


def enter_new_item_photo_window():
    return Window(
        Const("Отправьте фото товара"),
        MessageInput(
            func=selected.on_send_photo_for_new_item,
            content_types=ContentType.PHOTO,
        ),
        Back(Const("Назад")),
        state=states.CreateItem.send_photo,
    )


def confirm_new_item_create_window():
    return Window(
        Multi(
            Const("Подтвердите создание нового товара"),
            List(
                Format(
                    "<b>{name}</b>\n\nЦена: <code>{price} UAH</code>\n\n"
                    "<i>{desc}<"
                ),
                id="text_list",
                items="items_list",
            ),
            sep="\n\n",
        ),
        DynamicMedia(selector="photo"),
        Button(
            Const("Подтвердить"),
            id='save_new_item',
            on_click=selected.on_save_new_item,
        ),
        Back(Const("Назад")),
        state=states.CreateItem.confirm,
        getter=getters.new_item_getter,
    )



def select_edit_param_of_item_window():
    return Window(
        Const("Выберите параметр для редактирования"),
        keyboards.edit_item_kb(selected.on_select_edit_param),
        Back(Const("Назад")),
        state=states.EditItem.select_edit_param,
        getter=getters.item_edit_param_list_getter,
    )


def edit_item_name_window():
    return Window(
        Const("Введите новое название товара"),
        TextInput(id="new_name", on_success=selected.on_change_item_name),
        Cancel(Const("Отмена")),
        state=states.EditItemName.enter_new_name,
    )


def edit_item_price_window():
    return Window(
        Const("Введите новую цену товара в USDT"),
        TextInput(id="new_price", on_success=selected.on_change_item_price),
        Cancel(Const("Отмена")),
        state=states.EditItemPrice.enter_new_price,
    )


def edit_item_description_window():
    return Window(
        Const("Введите новое описание товара (до 500 символов)"),
        TextInput(id="new_description", on_success=selected.on_change_item_description),
        Cancel(Const("Отмена")),
        state=states.EditItemDescription.enter_new_description,
    )


def edit_item_photo_window():
    return Window(
        Const("Отправьте новое фото товара"),
        MessageInput(
            func=selected.on_send_new_photo_for_item,
            content_types=ContentType.PHOTO,
        ),
        Cancel(Const("Отмена")),
        state=states.EditItemPhoto.send_new_photo,
    )


def confirm_delete_item_window():
    return Window(
        Const("Вы уверены, что хотите удалить товар?"),
        Button(
            Const("Да"),
            id="delete_item",
            on_click=selected.on_confirm_delete_item,
        ),
        Cancel(Const("Нет")),
        state=states.DeleteItem.confirm,
    )


def edit_item_category_window():
    return Window(
        Const("Выберите новую категорию для товара"),
        categories_kb(selected.on_select_new_item_category),
        Cancel(Const("Назад")),
        state=states.EditItemCategory.select_new_category,
        getter=category_getter,
    )