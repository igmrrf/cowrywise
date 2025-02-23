from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['POST'])
def enroll_user():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'firstname', 'lastname']):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    user = User(
        email=data['email'],
        firstname=data['firstname'],
        lastname=data['lastname']
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User enrolled successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.lastname
        }
    }), 201

@user_routes.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'firstname': user.firstname,
        'lastname': user.lastname
    } for user in users])