"""
Keyboards manager
"""

from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from . import strings


def _create_keyboard(row_width=3) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)


_default_value = _create_keyboard(row_width=1)
_default_value.add('no_keyboard')


def get_keyboard(key: str) -> ReplyKeyboardMarkup:
    if key == 'remove':
        return ReplyKeyboardRemove()
    elif key == 'main_menu':
        main_menu_keyboard = _create_keyboard(row_width=1)
        main_menu_keyboard.add(strings.get_string('main_menu.categories'),
                               strings.get_string('main_menu.favorites'),
                               strings.get_string('main_menu.contacts'),
                               strings.get_string('main_menu.share'))
        return main_menu_keyboard
    else:
        return _default_value
