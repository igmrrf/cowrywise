import unittest
from app import create_app, db
from app.models.user import User

class TestUserRoutes(unittest.TestCase):
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

    def test_enroll_user(self):
        response = self.client.post('/users', json={
            'email': 'test@example.com',
            'firstname': 'Test',
            'lastname': 'User'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.query.filter_by(email='test@example.com').first())