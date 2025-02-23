from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.utils.errors import (
    ValidationError,
    LibraryError,
)

user_bp = Blueprint("user_routes", __name__)


@user_bp.route("/user", methods=["GET"])
def index():
    return jsonify({"health": "healthy"})


@user_bp.route("/users", methods=["POST"])
def enroll_user():
    data = request.get_json()

    if not all(k in data for k in ["email", "firstname", "lastname"]):
        raise ValidationError("Missing required fields")

    if db.session.query(User).filter_by(email=data["email"]).first():
        raise LibraryError("Email already registered", 400)

    user = User(
        email=data["email"], firstname=data["firstname"], lastname=data["lastname"]
    )

    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User enrolled successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                },
            }
        ),
        201,
    )


@user_bp.route("/users", methods=["GET"])
def list_users():
    users = db.session.query(User)
    return jsonify(
        [
            {
                "id": user.id,
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
            }
            for user in users
        ]
    )
