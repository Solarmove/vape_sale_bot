from aiogram_dialog import Dialog
from . import windows

admin_menu_dialogs_list = [
    Dialog(
        windows.admin_main_menu_window()
    ),
    Dialog(
        windows.waiter_menu_window()
    ),
    Dialog(
        windows.give_promo_window(),
        windows.confirm_give_promo_window(),
    ),
    Dialog(
        windows.give_prise_window(),
        windows.confirm_give_prise_window()
    ),
    Dialog(
        windows.add_waiter_window(),
        windows.confirm_add_waiter_window()
    ),
    Dialog(
        windows.delete_waiter_window(),
        windows.confirm_delete_waiter_window()
    ),
    Dialog(
        windows.waiters_list_window()
    ),
    Dialog(
        windows.stat_window()
    ),
    Dialog(
        windows.select_date_from_window(),
        windows.select_date_to_window()
    )
]
