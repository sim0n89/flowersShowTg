import sqlite3
from pathlib import Path
import os
import sys
from config_data.config import load_config


config = load_config()
path = Path("flowersShop", "db.sqlite3")
print(path)
conn = sqlite3.connect(path , check_same_thread=False)


def get_categories():
    print(os.path.dirname(sys.modules['__main__'].__file__))
    cursor = conn.cursor()
    sql = f"SELECT title FROM flowersShop_category"
    categories = cursor.execute(sql).fetchall()
    return categories
