import pytest
from app import create_app, db
from app.models.user import User


@pytest.fixture
def client():
    """Flask test client with a test database."""
    app = create_app()  # Assume a test config with SQLite in-memory
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_index(client):
    """Test the health check route."""
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json == {"health": "healthy"}


def test_enroll_user(client):
    """Test enrolling a new user successfully."""
    payload = {
        "email": "test@example.com",
        "firstname": "John",
        "lastname": "Doe",
    }
    response = client.post("/users", json=payload)

    assert response.status_code == 201
    assert response.json["message"] == "User enrolled successfully"
    assert response.json["user"]["email"] == "test@example.com"

    # Ensure the user is in the database
    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None
    assert user.firstname == "John"
    assert user.lastname == "Doe"


def test_enroll_user_missing_fields(client):
    """Test enrolling a user with missing fields."""
    payload = {"email": "incomplete@example.com"}  # Missing firstname & lastname
    response = client.post("/users", json=payload)

    assert response.status_code == 400
    assert "Missing required fields" in response.json["error"]


def test_enroll_user_duplicate_email(client):
    """Test enrolling a user with a duplicate email."""
    user = User(email="duplicate@example.com", firstname="Alice", lastname="Smith")
    db.session.add(user)
    db.session.commit()

    payload = {
        "email": "duplicate@example.com",
        "firstname": "Alice",
        "lastname": "Smith",
    }
    response = client.post("/users", json=payload)

    assert response.status_code == 400
    assert "Email already registered" in response.json["error"]


def test_list_users(client):
    """Test listing users."""
    user1 = User(email="user1@example.com", firstname="User", lastname="One")
    user2 = User(email="user2@example.com", firstname="User", lastname="Two")
    db.session.add_all([user1, user2])
    db.session.commit()

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["email"] == "user1@example.com"
    assert response.json[1]["email"] == "user2@example.com"
