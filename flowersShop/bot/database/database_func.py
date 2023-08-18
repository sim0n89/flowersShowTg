from sqlite3_api.field_types import CustomType
from sqlite3_api import Table


class Category(Table):
    id: int
    title: str


class Product(Table):
    id: int
    name: str
    created: str
    updated: str
    price: float
    description: str
    status: bool
    category: int
    image: str


class Client(Table):
    tlg_id: str
    name: str
    phone: str


class Order(Table):
    order_create: str
    product: int
    time_to_delievery: str
    address: str
    total_price: float
    client: int
    order_status: str
    


def get_product(category, price):
    