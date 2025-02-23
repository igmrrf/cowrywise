import requests
from flask import Blueprint, jsonify, request
from app.utils.errors import LibraryError
from app import db
from app.models.book import Book, BorrowedBook

admin_bp = Blueprint("admin_routes", __name__)

FRONTEND_API_URL = "http://frontend_api:5000"  # Will be used in Docker


def sync_with_frontend(action, data):
    try:
        response = requests.post(
            f"{FRONTEND_API_URL}/sync/books", json={"action": action, "book": data}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        return
        # raise self.retry(exc=exc, countdown=60)  # retry after 1 minute


@admin_bp.route("/admin/", methods=["GET"])
def index():
    return jsonify({"health": "healthy"})


@admin_bp.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    if not all(k in data for k in ["title", "author", "publisher", "category"]):
        return jsonify({"error": "Missing required fields"}), 400

    book = Book(
        title=data["title"],
        author=data["author"],
        publisher=data["publisher"],
        category=data["category"],
    )

    book = Book(title="fish")
    db.session.add(book)
    db.session.commit()

    # Sync with frontend API
    try:
        # Make sync asynchronous
        sync_with_frontend(
            "add",
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "category": book.category,
            },
        )
    except requests.exceptions.RequestException:
        # Log the error but don't fail the request
        pass

    return (
        jsonify(
            {
                "message": "Book added successfully",
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "publisher": book.publisher,
                    "category": book.category,
                },
            }
        ),
        201,
    )


@admin_bp.route("/books/<int:book_id>", methods=["DELETE"])
def remove_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    # Sync with frontend API
    try:
        requests.post(
            f"{FRONTEND_API_URL}/sync/books",
            json={"action": "delete", "book_id": book_id},
        )
    except requests.exceptions.RequestException:
        pass

    return jsonify({"message": "Book removed successfully"})


@admin_bp.route("/users", methods=["GET"])
def list_users():
    # Fetch users from frontend API
    try:
        response = requests.get(f"{FRONTEND_API_URL}/users")
        return jsonify(response.json())
    except requests.exceptions.RequestException:
        return jsonify({"error": "Unable to fetch users"}), 500


@admin_bp.route("/borrowed-books", methods=["GET"])
def list_borrowed_books():
    try:
        borrowed_books = BorrowedBook.query.all()
        return jsonify(
            [
                {
                    "book_id": record.book_id,
                    "book_title": record.book.title,
                    "user_email": record.user_email,
                    "borrow_date": record.borrow_date.isoformat(),
                    "return_date": record.return_date.isoformat(),
                }
                for record in borrowed_books
            ]
        )
    except Exception as e:
        raise LibraryError(f"Failed to fetch borrowed books: {str(e)}", 500)


@admin_bp.route("/unavailable-books", methods=["GET"])
def list_unavailable_books():
    try:
        unavailable_books = Book.query.filter_by(available=False).all()
        return jsonify(
            [
                {
                    "id": book.id,
                    "title": book.title,
                    "borrowed_by": (
                        book.borrowed_records[-1].user_email
                        if book.borrowed_records
                        else None
                    ),
                    "available_date": (
                        book.borrowed_records[-1].return_date.isoformat()
                        if book.borrowed_records
                        else None
                    ),
                }
                for book in unavailable_books
            ]
        )
    except Exception as e:
        raise LibraryError(f"Failed to fetch unavailable books: {str(e)}", 500)
