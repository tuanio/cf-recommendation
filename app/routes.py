from app.models import *
from app import app, db
from app.utils import make_response
from flask_cors import cross_origin
from sqlalchemy.sql import func
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    return make_response(dict(name="any"))


@app.route("/add-user", methods=["POST"])
@cross_origin()
def add_user():
    try:
        user_code = request.get_json(force=True).get("userId")
        user = User(user_code)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return make_response(dict(stauts="FAIL", detail=str(e)))
    return make_response(dict(status="SUCCESS"))


@app.route("/add-product", methods=["POST"])
@cross_origin()
def add_product():
    try:
        product_code = request.get_json(force=True).get("productId")
        product = Product(product_code)
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        return make_response(dict(stauts="FAIL", detail=str(e)))
    return make_response(dict(status="SUCCESS"))


@app.route("/add-order", methods=["POST"])
@cross_origin()
def add_order():
    try:
        data = request.get_json(force=True)
        user_code = data.get("userId")
        product_code = data.get("productId")
        rating = int(data.get("rating"))
        order = Order(user_code, product_code, rating)
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return make_response(dict(stauts="FAIL", detail=str(e)))
    return make_response(dict(status="SUCCESS"))


@app.route("/get-recommendation/<path:query_user_code>", methods=["GET"])
@cross_origin()
def get_recommendation(query_user_code: str):

    try:
        order = (
            db.session.query(
                Order.user_code, Order.product_code, func.avg(Order.rating).label("rating")
            )
            .group_by(Order.user_code, Order.product_code)
            .all()
        )

        order = [dict(item) for item in order]
        order = pd.DataFrame(order)

        list_user_code = order["user_code"].unique()
        list_product_code = order["product_code"].unique()

        user_item = np.zeros((len(list_user_code), len(list_product_code)))
        for user_idx, user_code in enumerate(list_user_code):
            for item_idx, product_code in enumerate(list_product_code):
                user_item[user_idx, item_idx] = order[
                    (order.user_code == user_code) & (order.product_code == product_code)
                ].rating.values[0]

        # ma trận similarity (len user) x (len user)
        similarity_matrix = cosine_similarity(user_item)

        # tìm index của user theo id
        user_idx = np.where(list_user_code == query_user_code)[0][0]
        
        list_product_recommendation = []
        # lặp qua tất cả sản phẩm hiện có
        for product_idx, product_code in enumerate(list_product_code):
            # tìm tất cả user đã rate sản phẩm đó
            user_rated_product = np.where(user_item[:, product_idx] > 0)[0]
            # nếu user hiện tại đã rate thì bỏ ra
            user_rated_product = user_rated_product[user_rated_product != user_idx]

            # tìm các hệ số tương quan giữa user mong muốn và tất cả user đã rate
            sim = similarity_matrix[user_idx, user_rated_product]
            sim = sim[sim < 1] # loại bỏ giá trị có tương quan là 1, vì nó tương quan với chính nó
            rating = user_item[user_rated_product, product_idx] # lấy list rating của những user đã rate

            # tính hệ số rating dự đoán, tổng trọng số giữa rating và độ tương quan
            r = (rating * sim).sum() / sim.sum()

            # đưa vào tuple (product id, rating) -> tí nữa sắp xếp giảm dần
            list_product_recommendation.append((product_code, r))

        # sắp xếp giảm dần theo rating dự đoán
        list_product_recommendation = sorted(list_product_recommendation, key=lambda x: x[1], reverse=True)
        list_product_recommendation = [pack[0] for pack in list_product_recommendation]

    except Exception as e:
        return make_response(dict(stauts="FAIL", detail=str(e)))

    return make_response(dict(status="SUCCESS", list_product_recommend_id=list_product_recommendation))
