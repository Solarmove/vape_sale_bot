from aiogram_dialog import Dialog
from . import windows


main_menu_dialogs_list = [
    Dialog(
        windows.send_phone_number(),
        windows.rules_window()
    ),
    Dialog(
        windows.user_qr_window(),
        
    ),
    Dialog(
        windows.enter_promocode_window()
    ), 
    Dialog(
        windows.my_cocktails_window()
    )
]