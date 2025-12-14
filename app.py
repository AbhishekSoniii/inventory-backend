from flask import Flask
from flask_cors import CORS
from extensions import db
from routes import product_routes
import os

app = Flask(__name__)
CORS(app)

db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///inventory.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(product_routes)

if __name__ == "__main__":
    app.run()
