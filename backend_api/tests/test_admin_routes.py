import unittest
from app import create_app, db
from app.models.book import Book

class TestAdminRoutes(unittest.TestCase):
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

    def test_add_book(self):
        response = self.client.post('/admin/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'publisher': 'Test Publisher',
            'category': 'Test Category'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Book.query.filter_by(title='Test Book').first())