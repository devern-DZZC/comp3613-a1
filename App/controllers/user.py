from App.models import User, Student, Staff
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password, type="student")
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_student(username, password):
    newuser = Student(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_staff(username, password):
    newuser = Staff(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def add_student_hours(student_id, hours):
    student = Student.query.get(student_id)
    if student:
        currentHours = student.hours
        newHours = currentHours + hours
        student.set_hours(newHours)
        db.session.add(student)
        db.session.commit()

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
