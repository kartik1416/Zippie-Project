from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from .schemas import UserSchema, UserRegisterSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

user_schema = UserSchema()
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    errors = register_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400
    hashed = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    # JWT identities should be simple (string). Put extra info into additional_claims.
    access_token = create_access_token(identity=str(user.id), additional_claims={'username': user.username, 'role': user.role})
    return jsonify({'access_token': access_token}), 200
