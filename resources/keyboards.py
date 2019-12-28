"""
Keyboards manager
"""

from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from . import strings
from typing import List
from filebot.models import Category, File


def _create_keyboard(row_width=3) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)


_default_value = _create_keyboard(row_width=1)
_default_value.add('no_keyboard')


def get_keyboard(key: str) -> ReplyKeyboardMarkup:
    if key == 'remove':
        return ReplyKeyboardRemove()
    elif key == 'main_menu':
        main_menu_keyboard = _create_keyboard(row_width=3)
        main_menu_keyboard.add(strings.get_string('main_menu.categories'),
                               strings.get_string('main_menu.favorites'),
                               strings.get_string('main_menu.search'),
                               strings.get_string('main_menu.upload'),
                               strings.get_string('main_menu.contacts'),
                               strings.get_string('main_menu.share'))
        return main_menu_keyboard
    elif key == 'search.index':
        search_keyboard = _create_keyboard(row_width=1)
        search_keyboard.add(strings.get_string('back'))
        return search_keyboard
    else:
        return _default_value


def from_categories_list_to_keyboard(categories: List[Category], include_from_users=False) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=2)
    keyboard.add(*[category.name for category in categories])
    if include_from_users:
        keyboard.add(strings.get_string('catalog.from_users'))
    keyboard.add(strings.get_string('back'))
    return keyboard


def from_files_list_to_keyboard(files: List[File]) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=2)
    keyboard.add(*[file.name for file in files])
    keyboard.add(strings.get_string('back'))
    return keyboard


def from_file_to_inline_keyboard_favorite(file: File, remove=False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    if not remove:
        favorite_button = InlineKeyboardButton(strings.get_string('catalog.add_favorite.add'), callback_data=str(file.id))
    else:
        favorite_button = InlineKeyboardButton(strings.get_string('catalog.add_favorite.remove'), callback_data=str(file.id))
    keyboard.add(favorite_button)
    return keyboard
