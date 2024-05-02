from . import db

class SquatExercise(db.Model):
    __tablename__ = 'squat_exercises'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), unique=True, nullable=False)
    correct = db.Column(db.Integer)
    incorrect = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    feedback = db.Column(db.JSON)  
