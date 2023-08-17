import sqlite3
from pathlib import Path
import os
import sys
from config_data.config import load_config
from os import path


config = load_config()

db_path = os.path.join(config.db.path)
conn = sqlite3.connect(db_path, check_same_thread=False)


def get_categories():
    cursor = conn.cursor()
    sql = f"SELECT title FROM flowersShop_category"
    categories = cursor.execute(sql).fetchall()
    return categories
