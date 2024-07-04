from aiogram.fsm.state import StatesGroup, State


class AdminMenu(StatesGroup):
    select_action = State()


class EditCategory(StatesGroup):
    select_category = State()
    select_edit_param = State()


class CreateCategory(StatesGroup):
    enter_name = State()


class ChangeCategoryName(StatesGroup):
    enter_new_name = State()


class DeleteCategory(StatesGroup):
    confirm = State()


class EditItem(StatesGroup):
    select_category = State()
    select_item = State()
    select_edit_param = State()


class CreateItem(StatesGroup):
    enter_name = State()
    enter_price = State()
    enter_description = State()
    send_photo = State()
    confirm = State()


class EditItemName(StatesGroup):
    enter_new_name = State()


class EditItemPrice(StatesGroup):
    enter_new_price = State()


class EditItemDescription(StatesGroup):
    enter_new_description = State()


class EditItemPhoto(StatesGroup):
    send_new_photo = State()


class DeleteItem(StatesGroup):
    confirm = State()


class EditItemCategory(StatesGroup):
    select_new_category = State()
