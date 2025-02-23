from datetime import datetime
import pytest
import requests
from unittest.mock import patch
from app import create_app, db
from app.models.book import Book, BorrowedBook


@pytest.fixture
def client():
    """Flask test client with app context and test database."""
    app = create_app()  # Assuming "testing" config uses SQLite in-memory DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_index(client):
    """Test the health check route."""
    response = client.get("/admin/")
    assert response.status_code == 200
    assert response.json == {"health": "healthy"}


def test_add_book(client, mocker):
    """Test adding a book."""
    mock_sync = mocker.patch("app.routes.admin_routes.sync_with_frontend")

    payload = {
        "title": "Test Book",
        "author": "John Doe",
        "publisher": "Test Publisher",
        "category": "Fiction",
    }

    response = client.post("/admin/books", json=payload)

    assert response.status_code == 201
    data = response.json
    assert data["message"] == "Book added successfully"
    assert data["book"]["title"] == "Test Book"

    # Ensure sync function was called
    mock_sync.assert_called_once_with(
        "add",
        {
            "id": data["book"]["id"],
            "title": "Test Book",
            "author": "John Doe",
            "publisher": "Test Publisher",
            "category": "Fiction",
        },
    )


def test_add_book_missing_fields(client):
    """Test adding a book with missing required fields."""
    payload = {"title": "Missing Author"}
    response = client.post("/admin/books", json=payload)
    assert response.status_code == 400
    assert "error" in response.json


def test_remove_book(client):
    """Test removing a book."""
    book = Book(title="To Delete", author="Unknown", publisher="XYZ", category="Sci-Fi")
    db.session.add(book)
    db.session.commit()

    response = client.delete(f"/admin/books/{book.id}")
    assert response.status_code == 200
    assert response.json == {"message": "Book removed successfully"}

    # Ensure the book is deleted
    assert db.session.get(Book, book.id) is None


@patch("requests.get")
def test_list_users(mock_get, client):
    """Test fetching users from frontend API."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": 1, "name": "User One"}]

    response = client.get("/admin/users")
    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "User One"}]


@patch("requests.get")
def test_list_users_failure(mock_get, client):
    """Test failure when frontend API is unavailable."""
    mock_get.side_effect = requests.exceptions.RequestException()

    response = client.get("/admin/users")
    assert response.status_code == 500
    assert response.json == {"error": "Unable to fetch users"}


def test_list_borrowed_books(client):
    """Test fetching borrowed books."""
    book = Book(
        title="Borrowed Book", author="Alice", publisher="XYZ", category="Drama"
    )
    db.session.add(book)
    db.session.commit()

    borrowed_book = BorrowedBook(
        book_id=book.id,
        user_email="user@example.com",
        borrow_date=datetime.now(),
        return_date=datetime.now(),
    )
    db.session.add(borrowed_book)
    db.session.commit()

    response = client.get("/admin/borrowed-books")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["book_title"] == "Borrowed Book"
    assert response.json[0]["user_email"] == "user@example.com"


def test_list_unavailable_books(client):
    """Test fetching unavailable books."""
    book = Book(
        title="Unavailable Book",
        author="Bob",
        publisher="XYZ",
        category="Mystery",
        available=False,
    )
    db.session.add(book)
    db.session.commit()

    response = client.get("/admin/unavailable-books")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Unavailable Book"
