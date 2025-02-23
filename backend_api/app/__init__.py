from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
import os

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="Library Admin API",
    version="1.0",
    description="Admin API for managing library books and users",
    doc="/docs",
)


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "postgresql://user:password@db:5432/backend_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    return app
