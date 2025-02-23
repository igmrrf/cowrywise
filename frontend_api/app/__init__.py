from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./testdb.db"
    # Database configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    from app.routes.user_routes import user_bp
    from app.routes.book_routes import book_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(book_bp)

    return app
