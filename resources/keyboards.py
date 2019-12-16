"""
Keyboards manager
"""

from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from . import strings
from typing import List
from filebot.models import Category, File


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


def from_categories_list_to_keyboard(categories: List[Category]) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=2)
    keyboard.add(*[category.name for category in categories])
    keyboard.add(strings.get_string('back'))
    return keyboard


def from_file_to_inline_keyboard_favorite(file: File) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    favorite_button = InlineKeyboardButton(strings.get_string('catalog.add_favorite'), callback_data=str(file.id))
    keyboard.add(favorite_button)
    return keyboard
