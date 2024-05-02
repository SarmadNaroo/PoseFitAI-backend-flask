from flask import Blueprint, request, jsonify
from app.models import db
from app.models.plank_exercise import PlankExercise
from flask_jwt_extended import jwt_required, current_user

plank_blueprint = Blueprint('plank', __name__)

@plank_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_or_update_plank():
    data = request.get_json()

    # Check if a plank exercise already exists for the current user
    existing_plank = PlankExercise.query.filter_by(
        user_id=current_user.id
    ).first()

    if existing_plank:
        # Increment the existing plank exercise counts
        existing_plank.correct += data.get('correct', 0)
        existing_plank.incorrect += data.get('incorrect', 0)
        
        # Merge the new feedback counts with the existing feedback
        new_feedback = data.get('feedback', {})
        for key, value in new_feedback.items():
            existing_plank.feedback[key] = existing_plank.feedback.get(key, 0) + value
        
        db.session.commit()
        return jsonify({'message': 'Plank exercise updated', 'id': existing_plank.id}), 200
    else:
        # Create a new plank exercise
        new_plank = PlankExercise(
            user_id=current_user.id,
            correct=data.get('correct', 0),
            incorrect=data.get('incorrect', 0),
            feedback=data.get('feedback', {})
        )
        db.session.add(new_plank)
        db.session.commit()
        return jsonify({'message': 'Plank exercise added', 'id': new_plank.id}), 201
