from .user import create_student, create_staff
from .activity import create_activity
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_student('bob', 'bobpass')
    create_student('rob', 'robpass')
    create_student('jim', 'jimpass')
    create_student('phil', 'philpass')
    create_staff('dean', 'deanpass')
    create_staff('teacher', 'teacherpass')
    create_activity("community_service")
    create_activity("volunteering")
    create_activity("help_desk")
