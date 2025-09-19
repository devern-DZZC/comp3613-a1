from .user import create_student, create_staff
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_student('bob', 'bobpass')
    create_staff('pam', 'pampass')
