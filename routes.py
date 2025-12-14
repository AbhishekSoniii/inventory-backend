from flask import Blueprint, request, jsonify
from extensions import db
from models import Product

product_routes = Blueprint("product_routes", __name__)

# Add product
@product_routes.route("/products", methods=["POST"])
def add_product():
    product = Product(**request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added"})

# Get all products
@product_routes.route("/products", methods=["GET"])
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

# Mark as sold
@product_routes.route("/products/<int:id>/sell", methods=["PUT"])
def sell_product(id):
    p = Product.query.get_or_404(id)
    data = request.json
    p.sell_price = data["sell_price"]
    p.sell_date = data["sell_date"]
    p.sell_to = data.get("sell_to")
    p.status = "SOLD"
    db.session.commit()
    return jsonify({"message": "Product sold"})

  