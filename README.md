# Mock recommender system

# Dữ liệu cho app
Cần phải có 3 file, để trong thư mục data:
- `user.json` là file thông tin toàn bộ user trên hệ thống.
- `product.json` là file thông tin toàn bộ product trên hệ thống.
- `order.json` là file thông tin toàn bộ thông tin đặt hàng của hệ thống.

# How to run?
- B1: Tạo môi trường ảo với `python -m venv venv`.
- B2: Activate môi trường ảo
    - Trên windows: `venv/Script/activate`
    - Trên Linux: `source venv\bin\activate`
- B3: Cài các thư viện cần thiết bằng `pip install -r requirements.txt`
- B4: Set các biến môi trường.
- B5: Import dữ liệu bằng cách chạy file `python import_data.py`, phải đảm bảo có đủ 3 file dữ liệu trong thư mục `data`.
- B6: chạy bằng `flask run`.

# Các api hỗ trợ
- `/add-user`, methods: `POST`: api thêm user mới, nhận một key `userId` là id của User.
- `/add-product`, methods: `POST`: api thêm product mới, nhận một key `productId`, là id của Product.
- `/add-order`, methods: `POST`: api thêm một order, nhận 3 key: `userId`, `productId`, `rating` là id của User, id của Product và rating của user cho product đấy.
- `/get-recommendation/<query_user_code>`, methods: `GET`. `query_user_code` là id của user mong muốn lấy danh sách recommend. API sẽ trả về tất cả sản phẩm được gợi ý.

# Environment Variables
- `DATABASE_URL`: link kết nối đến database
- `FLASK_ENV`
- `FLASK_APP=app`

# Cách setup
- Chạy `python import_data.py` khi kết nối xong với database online

# Backend URL:
- `https://cf-project-production.up.railway.app`