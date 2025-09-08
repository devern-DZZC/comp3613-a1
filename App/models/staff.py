from App.database import db
from .user import User

class Staff(User):
    __tablename__ = 'staff'
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }