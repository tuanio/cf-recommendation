import json
from app import db
from app.models import *

db.drop_all()
db.create_all()

user = json.load(open("data/user.json", "r", encoding="utf-8"))
product = json.load(open("data/product.json", "r", encoding="utf-8"))
order = json.load(open("data/order.json", "r", encoding="utf-8"))

list_user_code = [User(data["_id"]) for data in user]
list_product_code = [Product(data["_id"]) for data in product]

db.session.bulk_save_objects(list_user_code)
db.session.bulk_save_objects(list_product_code)

db.session.commit()

list_order_items = []
for item in order:
    user_code = item["userId"]
    for product in item["orderItems"]:
        product_code = product["productId"]
        rating = product["rating"]
        order_object = Order(user_code, product_code, rating)
        list_order_items.append(order_object)

db.session.bulk_save_objects(list_order_items)
db.session.commit()
