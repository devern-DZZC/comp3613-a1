from App.database import db
from .user import User

class Student(User):
    __tablename__ = 'student'
    hours = db.Column(db.Integer, nullable=False, default=0)
    accolade = db.Column(db.String(120), nullable=False, default='')
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password):
        super().__init__(username, password)
    
    def set_hours(self, hours):
        self.hours = hours