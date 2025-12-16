import os
from flask import Flask
from flask_cors import CORS
from extensions import db
from routes import product_routes

app = Flask(__name__)
CORS(app)

# ---- DATABASE CONFIG ----
db_url = os.environ.get("DATABASE_URL")

if db_url:
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ---- REGISTER ROUTES (CRITICAL) ----
app.register_blueprint(product_routes)

# ---- HEALTH CHECK ----
@app.route("/")
def home():
    return {"status": "backend running"}

# ---- CREATE TABLES ON STARTUP ----
with app.app_context():
    db.create_all()
