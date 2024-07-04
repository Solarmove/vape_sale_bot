from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    select_action = State()


class Store(StatesGroup):
    select_category = State()
    select_item = State()
    show_item = State()


class Purchase(StatesGroup):
    select_currency = State()
    create_invoice = State()
    finnal_msg = State()
