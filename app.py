import os
import time
from flask import Flask, jsonify, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user

# --- Flask app ---
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-prod")

# --- Database ---
db_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Auth (basic) ---
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None

# --- Blueprints auto-register (imgbb_auto / auth_auto) ---
# If files exist in project root, they will import and attach themselves to `app`.
try:
    import imgbb_auto  # noqa: F401
except Exception as _e:
    pass

try:
    import auth_auto  # noqa: F401
except Exception as _e:
    pass

# --- Routes ---
@app.get("/")
def index():
    return render_template("index.html", user=current_user if hasattr(current_user, "is_authenticated") else None)

@app.get("/healthz")
def healthz():
    return jsonify(ok=True, ts=int(time.time()))

# DB ping for Render health diagnostics
from sqlalchemy import text as _sql_text
@app.get("/db-ping")
def db_ping():
    try:
        with db.engine.connect() as conn:
            val = conn.execute(_sql_text("SELECT 1")).scalar()
        return jsonify(ok=True, result=int(val))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 200

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")), debug=False)

@app.get("/uploader")
def uploader():
    return render_template("uploader.html")
