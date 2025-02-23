from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import app.utils

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./testdb.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
