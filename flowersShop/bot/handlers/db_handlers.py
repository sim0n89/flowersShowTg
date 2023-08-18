import sqlite3
from pathlib import Path
import os
import sys
from config_data.config import load_config
from os import path


config = load_config()
root_dir = Path(__file__).parent.parent.parent
db_path = os.path.join(root_dir,config.db.path)
conn = sqlite3.connect(db_path, check_same_thread=False)


def get_categories():
    cursor = conn.cursor()
    sql = f"SELECT title FROM flowersShop_category"
    categories = cursor.execute(sql).fetchall()
    cursor.close()
    return categories


def get_product(category, price):
    cursor = conn.cursor()
    sql = f"""SELECT p.name, p.description, p.price, i.image FROM flowersShop_product p
LEFT JOIN flowersShop_product_product_to_category ptc ON(ptc.product_id = p.id)
LEFT JOIN flowersShop_category c ON(c.id = ptc.id)
LEFT JOIN flowersShop_product_images pti ON(p.id = pti.product_id)
LEFT JOIN flowersShop_image i ON(i.id = pti.image_id)
WHERE c.title = '{category}' and p.price<{float(price)}"""
    product = cursor.execute(sql).fetchone()
    cursor.close()
    return product
    