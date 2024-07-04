import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Select, Back, Calendar
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format

from bot.dialogs.admin_menu import states, selected, getters, keyboards
from bot.utils.i18n_utils.i18n_format import I18nFormat


