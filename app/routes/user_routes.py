from flask import Blueprint, jsonify
from app.models.user import User
from app.models import db

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'weight': user.weight,
        'height': user.height
    } for user in users]

    return jsonify(users_list), 200
