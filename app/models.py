from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, user_code: str):
        self.user_code = user_code


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, product_code: str):
        self.product_code = product_code


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.String(255), nullable=False)
    product_code = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, user_code: str, product_code: str, rating: float):
        self.user_code = user_code
        self.product_code = product_code
        self.rating = rating
