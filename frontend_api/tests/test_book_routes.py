import pytest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models.book import Book, BorrowedBook
from app.models.user import User


@pytest.fixture
def client():
    """Flask test client with a test database."""
    app = create_app("testing")  # Assume a test config with SQLite in-memory
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_index(client):
    """Test the health check route."""
    response = client.get("/book")
    assert response.status_code == 200
    assert response.json == {"health": "healthy"}


def test_list_books(client):
    """Test listing available books."""
    book1 = Book(
        title="Book One",
        author="Author A",
        publisher="Pub A",
        category="Fiction",
        available=True,
    )
    book2 = Book(
        title="Book Two",
        author="Author B",
        publisher="Pub B",
        category="Non-fiction",
        available=True,
    )
    db.session.add_all([book1, book2])
    db.session.commit()

    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["title"] == "Book One"
    assert response.json[1]["title"] == "Book Two"


def test_get_book(client):
    """Test retrieving a book by ID."""
    book = Book(
        title="Book Test",
        author="Author X",
        publisher="Pub X",
        category="Sci-Fi",
        available=True,
    )
    db.session.add(book)
    db.session.commit()

    response = client.get(f"/books/{book.id}")
    assert response.status_code == 200
    assert response.json["title"] == "Book Test"


def test_get_book_not_found(client):
    """Test retrieving a non-existent book."""
    response = client.get("/books/999")
    assert response.status_code == 404  # Should return a 404 Not Found


def test_borrow_book(client):
    """Test borrowing a book successfully."""
    book = Book(
        title="Borrowable Book",
        author="Alice",
        publisher="XYZ",
        category="Drama",
        available=True,
    )
    user = User(id=1, name="Test User", email="test@example.com")
    db.session.add_all([book, user])
    db.session.commit()

    payload = {"user_id": 1, "days": 7}
    response = client.post(f"/books/{book.id}/borrow", json=payload)

    assert response.status_code == 200
    assert response.json["message"] == "Book borrowed successfully"

    # Ensure the book is marked as unavailable
    assert Book.query.get(book.id).available is False


def test_borrow_book_already_borrowed(client):
    """Test trying to borrow an already borrowed book."""
    book = Book(
        title="Unavailable Book",
        author="Bob",
        publisher="XYZ",
        category="Mystery",
        available=False,
    )
    user = User(id=2, name="Test User", email="test@example.com")
    db.session.add_all([book, user])
    db.session.commit()

    payload = {"user_id": 2, "days": 5}
    response = client.post(f"/books/{book.id}/borrow", json=payload)

    assert response.status_code == 400  # Expect an error since the book is unavailable


def test_borrow_book_invalid_user(client):
    """Test borrowing a book with a non-existent user."""
    book = Book(
        title="Test Book",
        author="Test Author",
        publisher="Test Pub",
        category="Test",
        available=True,
    )
    db.session.add(book)
    db.session.commit()

    payload = {"user_id": 999, "days": 3}  # Non-existent user ID
    response = client.post(f"/books/{book.id}/borrow", json=payload)

    assert response.status_code == 404  # Should return 404 Not Found


def test_borrow_book_invalid_days(client):
    """Test borrowing a book with invalid number of days."""
    book = Book(
        title="Another Book",
        author="XYZ",
        publisher="ABC",
        category="History",
        available=True,
    )
    user = User(id=3, name="User Three", email="three@example.com")
    db.session.add_all([book, user])
    db.session.commit()

    payload = {"user_id": 3, "days": -5}  # Invalid days
    response = client.post(f"/books/{book.id}/borrow", json=payload)

    assert response.status_code == 400
    assert "Borrow days must be positive" in response.json["error"]


def test_sync_books_add(client):
    """Test syncing a book addition."""
    payload = {
        "action": "add",
        "book": {
            "id": 10,
            "title": "Synced Book",
            "author": "Sync Author",
            "publisher": "Sync Pub",
            "category": "Sync Cat",
        },
    }

    response = client.post("/sync/books", json=payload)
    assert response.status_code == 200
    assert response.json == {"message": "Sync successful"}

    book = Book.query.get(10)
    assert book is not None
    assert book.title == "Synced Book"


def test_sync_books_delete(client):
    """Test syncing a book deletion."""
    book = Book(
        id=20,
        title="To Be Deleted",
        author="Delete Me",
        publisher="Del Pub",
        category="Del Cat",
    )
    db.session.add(book)
    db.session.commit()

    payload = {"action": "delete", "book_id": 20}
    response = client.post("/sync/books", json=payload)

    assert response.status_code == 200
    assert response.json == {"message": "Sync successful"}

    book = Book.query.get(20)
    assert book is None  # Ensure book is deleted
