from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database.database_sql_func import get_categories

def start_keyboard():
    categories = get_categories()
    button_data = categories
    button_data.append(('Другой повод',))
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )


def amount_keyboard():
    button_data = [
        ("~500", "~1000"),
        ("~2000", "Больше"),
        ("Не важно",),
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )


def buy_keyboard():
    button_data = [
        ("Заказать букет",),
        ("Заказать консультацию", "Посмотреть всю коллекцию"),
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )
