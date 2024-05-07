from flask import Blueprint, request, jsonify
from app.models.session_history import SessionHistory
from app.models import db
from datetime import datetime
from flask_jwt_extended import jwt_required, current_user

session_blueprint = Blueprint('session', __name__)

@session_blueprint.route('/start', methods=['POST'])
@jwt_required()
def start_session():
    if not request.json or 'exercise_name' not in request.json:
        return jsonify({'error': 'Missing exercise name'}), 400

    exercise_name = request.json['exercise_name']

    try:
        new_session = SessionHistory(
            user_id=current_user.id,
            exercise_name=exercise_name,
            start_time=datetime.utcnow(),
            completed=False
        )
        db.session.add(new_session)
        db.session.commit()
        return jsonify({'message': 'Session started', 'id': new_session.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@session_blueprint.route('/update', methods=['POST'])
@jwt_required()
def update_session():
    # Fetch the most recent session for the current user
    session = SessionHistory.query.filter_by(user_id=current_user.id).order_by(SessionHistory.start_time.desc()).first()
    
    # Check if the session is either non-existent or already completed
    if not session or session.completed:
        return jsonify({'message': 'No active session found to update'}), 404
    
    data = request.get_json()
    session.correct = data.get('correct', session.correct)
    session.incorrect = data.get('incorrect', session.incorrect)
    session.end_time = datetime.utcnow()  # Continuously update end time
    session.duration = (session.end_time - session.start_time).seconds

    db.session.commit()
    return jsonify({'message': 'Session updated', 'id': session.id}), 200

@session_blueprint.route('/end', methods=['POST'])
@jwt_required()
def end_session():
    # Fetch the most recent session for the current user
    session = SessionHistory.query.filter_by(user_id=current_user.id).order_by(SessionHistory.start_time.desc()).first()
    
    # Check if the session is either non-existent or already completed
    if not session or session.completed:
        return jsonify({'message': 'No active session found to end'}), 404
    
    data = request.get_json()
    session.correct = data.get('correct', session.correct)
    session.incorrect = data.get('incorrect', session.incorrect)
    session.completed = True
    session.end_time = datetime.utcnow()  # Mark final end time
    session.duration = (session.end_time - session.start_time).seconds

    db.session.commit()
    return jsonify({'message': 'Session ended', 'id': session.id, 'duration': session.duration}), 200

@session_blueprint.route('/all', methods=['GET'])
@jwt_required()
def get_sessions():
    sessions = SessionHistory.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': session.id,
        'exercise_name': session.exercise_name,
        'start_time': session.start_time.isoformat() if session.start_time else None,
        'end_time': session.end_time.isoformat() if session.end_time else None,
        'duration': session.duration,
        'correct': session.correct,
        'incorrect': session.incorrect,
    } for session in sessions]), 200