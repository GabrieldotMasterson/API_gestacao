"""
app/__init__.py — Flask application factory for Vercel serverless.

KEY DIFFERENCES from local dev:
  - SQLite → PostgreSQL (via DATABASE_URL env var from Neon/Supabase/Railway)
  - db.create_all() on first request instead of flask_migrate
  - No debug mode
  - CORS configured for production domain
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
import os
import logging

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

# Module-level flag to avoid running create_all() on every request
_tables_created = False

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)

    # ── Configuration ─────────────────────────────────────────────────────────
    app.config["SECRET_KEY"]     = os.environ["SECRET_KEY"]
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # PostgreSQL (required in production). SQLite for local fallback only.
    database_url = os.environ.get("DATABASE_URL", "sqlite:///gestacao.db")
    # Heroku/Render/Neon prefix fix: postgres:// → postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Connection pooling for serverless: close connections after each request
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": (
            {"sslmode": "require"} if "postgresql" in database_url else {}
        ),
    }

    # ── Swagger — parse=False prevents 422 interception ───────────────────────
    Swagger(app, template={
        "swagger": "2.0",
        "info": {"title": "Gestação API", "version": "2.0.0"},
        "host": os.environ.get("VERCEL_URL", "localhost:5000"),
        "basePath": "/",
        "schemes": ["https", "http"],
        "securityDefinitions": {
            "BearerAuth": {"type": "apiKey", "name": "Authorization", "in": "header"}
        },
    }, config={
        "headers": [],
        "specs": [{"endpoint": "apispec", "route": "/apispec.json"}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
    }, parse=False)

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)

    # Allow production frontend + local dev origins
    allowed_origins = [
        o.strip() for o in
        os.environ.get("ALLOWED_ORIGINS", "http://localhost,http://10.0.2.2").split(",")
        if o.strip()
    ]
    CORS(app, origins=allowed_origins + ["*"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"])

    # ── Models ────────────────────────────────────────────────────────────────
    from app.models.user          import User
    from app.models.message       import Message, Category
    from app.models.saved_message import SavedMessage
    from app.models.user_progress import UserProgress
    from app.models.reminder      import Reminder

    # ── Auto-create tables on first request (replaces flask_migrate on Vercel) ─
    @app.before_request
    def ensure_tables():
        global _tables_created
        if not _tables_created:
            try:
                db.create_all()
                _tables_created = True
                logger.info("Database tables verified/created")
            except Exception as e:
                logger.error(f"Failed to create tables: {e}")

    # ── JWT loaders ───────────────────────────────────────────────────────────
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id) if hasattr(user, "id") else str(user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_header, jwt_data):
        try:
            return db.session.get(User, int(jwt_data.get("sub", "")))
        except (ValueError, TypeError):
            return None

    @jwt.invalid_token_loader
    def invalid_token_cb(reason):
        return jsonify({"msg": f"Token inválido: {reason}"}), 422

    @jwt.unauthorized_loader
    def missing_token_cb(reason):
        return jsonify({"msg": "Autenticação necessária"}), 401

    @jwt.expired_token_loader
    def expired_token_cb(_h, _d):
        return jsonify({"msg": "Token expirado. Faça login novamente."}), 401

    @jwt.revoked_token_loader
    def revoked_token_cb(_h, _d):
        return jsonify({"msg": "Token revogado."}), 401

    # ── Blueprints ────────────────────────────────────────────────────────────
    from app.controllers.auth      import auth_bp
    from app.controllers.users     import users_bp
    from app.controllers.messages  import messages_bp
    from app.controllers.pregnancy import pregnancy_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(pregnancy_bp)

    @app.get("/health")
    def health():
        """
        Health check
        ---
        tags: [Sistema]
        responses:
          200:
            description: OK
        """
        return jsonify({"status": "ok", "version": "2.0.0",
                        "env": os.environ.get("FLASK_ENV", "development")})

    return app
