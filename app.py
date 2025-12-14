from flask import Flask
from flask_cors import CORS
from extensions import db

app = Flask(__name__)
CORS(app)

import os

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///inventory.db"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import Product
from routes import product_routes

app.register_blueprint(product_routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
