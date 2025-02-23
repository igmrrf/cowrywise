from app import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)  # Add index
    author = db.Column(db.String(100), nullable=False, index=True)  # Add index
    publisher = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)  # Add index
    available = db.Column(db.Boolean, default=True, index=True)  # Add index
    created_at = db.Column(db.DateTime, default=datetime.now())
    borrowed_records = db.relationship("BorrowedBook", backref="book", lazy=True)

class BorrowedBook(db.Model):
    __tablename__ = "borrowedbooks"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False, index=True)  # Add index
    user_id = db.Column(db.Integer, nullable=False, index=True)  # Add index
    user_email = db.Column(db.String(120), nullable=False, index=True)  # Add index
    borrow_date = db.Column(db.DateTime, default=datetime.now(), index=True)  # Add index
    return_date = db.Column(db.DateTime, nullable=False, index=True)  # Add index

    def get_id(self):
        return self.id

