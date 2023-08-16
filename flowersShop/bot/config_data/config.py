import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class AdminIDs:
    ids: list  # список телеграм id админов


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    # db_host: str          # URL-адрес базы данных
    # db_user: str          # Username пользователя базы данных
    # db_password: str      # Пароль к базе данных


@dataclass
class TelegramBot:
    token: str
    # admin_ids: list  # Список id администраторов бота


@dataclass
class Config:
    telegram_bot: TelegramBot
    # admin_ids: AdminIDs
    # db: DatabaseConfig


# @dataclass
def load_config():
    load_dotenv()
    return Config(
        telegram_bot=TelegramBot(token=os.getenv('TELEGRAM_TOKEN')),
        # admin_ids=AdminIDs(ids=os.getenv('ADMIN_IDS')),
        # db=DatabaseConfig(database=env('DATABASE_NAME')),
    )