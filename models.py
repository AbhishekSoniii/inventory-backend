from extensions import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    type = db.Column(db.String(20))
    model = db.Column(db.String(100))
    serial_no = db.Column(db.String(100))
    imei = db.Column(db.String(20))
    buy_price = db.Column(db.Float)
    sell_price = db.Column(db.Float)
    buy_date = db.Column(db.String(20))
    sell_date = db.Column(db.String(20))
    buy_from = db.Column(db.String(100))
    sell_to = db.Column(db.String(100))
    status = db.Column(db.String(20), default="IN_STOCK")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
