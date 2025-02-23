from flask import Blueprint, request, jsonify
from app.models.book import Book, BorrowedBook
from app.models.user import User
from app import db
from datetime import datetime, timedelta
from shared.errors import BookNotAvailableError, ResourceNotFoundError, ValidationError

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('/books', methods=['GET'])
def list_books():
    publisher = request.args.get('publisher')
    category = request.args.get('category')
    
    query = Book.query.filter_by(available=True)
    
    if publisher:
        query = query.filter_by(publisher=publisher)
    if category:
        query = query.filter_by(category=category)
        
    books = query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'category': book.category
    } for book in books])

@book_routes.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'category': book.category,
        'available': book.available
    })

@book_routes.route('/books/<int:book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("No JSON data provided")
            
        if 'user_id' not in data or 'days' not in data:
            raise ValidationError("Missing required fields: user_id and days")
            
        book = Book.query.get(book_id)
        if not book:
            raise ResourceNotFoundError("Book", book_id)
            
        user = User.query.get(data['user_id'])
        if not user:
            raise ResourceNotFoundError("User", data['user_id'])
        
        if not book.available:
            raise BookNotAvailableError(book_id)
            
        try:
            borrow_days = int(data['days'])
            if borrow_days <= 0:
                raise ValidationError("Borrow days must be positive")
        except ValueError:
            raise ValidationError("Days must be a valid number")
        
        return_date = datetime.utcnow() + timedelta(days=borrow_days)
        
        borrowed_book = BorrowedBook(
            book_id=book.id,
            user_id=user.id,
            return_date=return_date
        )
        
        book.available = False
        db.session.add(borrowed_book)
        db.session.commit()
        
        return jsonify({
            'message': 'Book borrowed successfully',
            'return_date': return_date.isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        if not isinstance(e, LibraryError):
            raise ValidationError("An unexpected error occurred")
        raise

@book_routes.route('/sync/books', methods=['POST'])
def sync_books():
    data = request.get_json()
    
    if data['action'] == 'add':
        book_data = data['book']
        book = Book(
            id=book_data['id'],
            title=book_data['title'],
            author=book_data['author'],
            publisher=book_data['publisher'],
            category=book_data['category']
        )
        db.session.add(book)
    
    elif data['action'] == 'delete':
        book = Book.query.get(data['book_id'])
        if book:
            db.session.delete(book)
    
    db.session.commit()
    return jsonify({'message': 'Sync successful'})