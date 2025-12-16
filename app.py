import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from extensions import db
from models import Product

app = Flask(__name__)
CORS(app)

# ---------- DATABASE ----------
db_url = os.environ.get("DATABASE_URL")
if db_url:
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ---------- HEALTH CHECK ----------
@app.route("/")
def home():
    return {"status": "backend running"}

# ---------- PRODUCTS ROUTES ----------
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "product_name": p.product_name,
            "type": p.type,
            "model": p.model,
            "imei": p.imei,
            "serial_no": p.serial_no,
            "status": p.status,
            "buy_price": p.buy_price,
            "sell_price": p.sell_price,
            "buy_date": p.buy_date,
            "sell_date": p.sell_date
        } for p in products
    ])

@app.route("/products", methods=["POST"])
def add_product():
    product = Product(**request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added"})

@app.route("/products/<int:id>/sell", methods=["PUT"])
def sell_product(id):
    p = Product.query.get_or_404(id)
    data = request.json
    p.sell_price = data["sell_price"]
    p.sell_date = data["sell_date"]
    p.sell_to = data.get("sell_to")
    p.status = "SOLD"
    db.session.commit()
    return jsonify({"message": "Product sold"})

# ---------- CREATE TABLES ----------
with app.app_context():
    db.create_all()
