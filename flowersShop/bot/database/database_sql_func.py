import sqlite3
from sqlite3 import Error
from pathlib import Path
import os
import sys
from config_data.config import load_config
import datetime

config = load_config()
root_dir = Path(__file__).parent.parent.parent
db_path = os.path.join(root_dir, config.db.path)


def create_connection(db_path=db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
    except Error as e:
        print(e)
    return conn


def get_categories():
    conn = create_connection()
    cursor = conn.cursor()
    with conn:
        sql = f"SELECT title FROM flowersShop_category"
        categories = cursor.execute(sql).fetchall()
    conn.close()
    return categories


def get_product(category, showed_products, amount):
    match amount:
        case "~500":
            sql_price = " AND p.price < 500"
        case "~1000":
            sql_price = " AND p.price <= 1000 AND p.price >= 500"
        case "~2000":
            sql_price = " AND p.price <= 2000 AND p.price > 1000"
        case "Больше":
            sql_price = " AND p.price > 2000"
        case "Не важно":
            sql_price = ""

    showed_slq = ""
    if len(showed_products) > 0:
        showed_slq = f" AND p.id NOT IN ({ ','.join(map(str, showed_products))})"

    amount = amount.replace("~", "")
    sql = f"""SELECT p.id,p.name, p.price, p.description, p.image FROM flowersShop_product p
LEFT JOIN flowersShop_product_category pc ON (p.id = pc.product_id)
LEFT JOIN flowersShop_category c ON (c.id = pc.category_id)
WHERE c.title = '{category}' {sql_price} {showed_slq}"""
    conn = create_connection()
    cursor = conn.cursor()
    with conn:
        product = cursor.execute(sql).fetchone()
    if product:
        product_dict = {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "description": product[3],
            "image": product[4],
        }
        return product_dict
    return False


def check_user(tlg_id, name="", phone=""):
    conn = create_connection()
    cursor = conn.cursor()
    with conn:
        sql = f"SELECT id FROM flowersShop_client WHERE tlg_id='{tlg_id}'"
        client = cursor.execute(sql).fetchone()
        if client is None:
            sql = (
                "INSERT INTO flowersShop_client (tlg_id, name, phone) VALUES (?, ?, ?)"
            )
            data = (tlg_id, name, phone)
            cursor.execute(sql, data)
            conn.commit()
            client_id = cursor.lastrowid
            return (client_id)
        return client[0]


def new_order(user_tlg, product_id, price, adress, date, time):
    user_id = check_user(user_tlg)
    conn = create_connection()
    cursor = conn.cursor()
    date_to_delievery = f"{date} {time}" 
    date_to_delievery = datetime.datetime.strptime(date_to_delievery,"%d.%m.%Y %H:%M")
    with conn:
        sql = """INSERT INTO flowersShop_order (order_create, time_to_delievery, address, total_price, order_status, client_id, product_id) 
        VALUES (?,?,?,?,?,?,?)"""
        data = (datetime.datetime.now(), date_to_delievery, adress, price, "new", user_id, product_id)
        cursor.execute(sql, data)
        conn.commit()
    conn.close()