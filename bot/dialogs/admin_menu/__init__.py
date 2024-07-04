from aiogram_dialog import Dialog
from . import windows

admin_menu_dialogs_list = [
    Dialog(
        windows.admin_menu_window()
    ),
    Dialog(
        windows.edit_category_window(),
        windows.select_edit_category_param_window(),
    ),
    Dialog(
        windows.add_category_window(),
    ),
    Dialog(
        windows.change_category_name_window(),
    ),
    Dialog(
        windows.delete_category_window(),
    ),
    Dialog(
        windows.edit_item_window(),
        windows.select_item_for_edit_window(),
        windows.select_edit_param_of_item_window(),
    ),
    Dialog(
        windows.enter_new_item_name_window(),
        windows.enter_new_item_price_window(),
        windows.enter_new_item_description_window(),
        windows.enter_new_item_photo_window(),
        windows.confirm_new_item_create_window(),
    ),
    Dialog(
        windows.edit_item_name_window(),
    ),
    Dialog(
        windows.edit_item_price_window(),
    ),
    Dialog(
        windows.edit_item_description_window(),
    ),
    Dialog(
        windows.edit_item_photo_window(),
    ),
    Dialog(
        windows.confirm_delete_item_window(),
    ),
    Dialog(
        windows.edit_item_category_window(),
    ),


]
