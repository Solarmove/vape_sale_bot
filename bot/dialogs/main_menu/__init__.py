from aiogram_dialog import Dialog
from . import windows


main_menu_dialogs_list = [
    Dialog(windows.main_menu_window()),
    Dialog(windows.store_window(), windows.items_in_category_window()),
    Dialog(windows.select_currency_window(), windows.create_invoice_window()),
]
