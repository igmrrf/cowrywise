import unittest
from app import create_app, db
from app.models.book import Book
from datetime import datetime, timedelta

class TestBookRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_filter_books(self):
        # Create test books
        books = [
            Book(title='Book 1', author='Author 1', publisher='Wiley', category='technology'),
            Book(title='Book 2', author='Author 2', publisher='Manning', category='fiction'),
            Book(title='Book 3', author='Author 3', publisher='Wiley', category='science')
        ]
        for book in books:
            db.session.add(book)
        db.session.commit()

        # Test publisher filter
        response = self.client.get('/books?publisher=Wiley')
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['publisher'], 'Wiley')

        # Test category filter
        response = self.client.get('/books?category=fiction')
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['category'], 'fiction')