from flask import Blueprint, request, jsonify
from app.models.session_history import SessionHistory
from app.models import db
from datetime import datetime
from flask_jwt_extended import jwt_required, current_user

session_blueprint = Blueprint('session', __name__)

@session_blueprint.route('/all', methods=['GET'])
@jwt_required()
def get_sessions():
    # Retrieve only sessions associated with the current user
    sessions = SessionHistory.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': session.id,
        'user_id': session.user_id,
        'exercise_name': session.exercise_name,
        'start_time': session.start_time.isoformat(),
        'end_time': session.end_time.isoformat(),
        'duration': session.duration,
        'correct': session.correct,
        'incorrect': session.incorrect
    } for session in sessions]), 200

@session_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_session():
    data = request.get_json()
    # Using current_user.id to ensure the session is added for the authenticated user
    new_session = SessionHistory(
        user_id=current_user.id,  # This ensures the session is associated with the logged-in user
        exercise_name=data.get('exercise_name'),
        start_time=datetime.fromisoformat(data.get('start_time')),  # Ensuring to use .get for safer extraction
        end_time=datetime.fromisoformat(data.get('end_time')),
        duration=data.get('duration', (datetime.fromisoformat(data.get('end_time')) - datetime.fromisoformat(data.get('start_time'))).seconds),
        correct=data.get('correct', 0),
        incorrect=data.get('incorrect', 0)
    )

    db.session.add(new_session)
    db.session.commit()

    return jsonify({'id': new_session.id}), 201
