from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from handlers.db_handlers import get_categories


def start_keyboard():
    categories = get_categories()
    button_data = [
        ("День рождения", "Свадьба"),
        ("В школу", "Без повода"),
        ("Другой повод",),
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )

def summ_keyboard():
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
        ("Заказать консультацию", "Посмотреть всю коллекцию")
    ]
     return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )

