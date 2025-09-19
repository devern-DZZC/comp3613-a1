from App.database import db

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    hours = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student", backref='request')

    def __init__(self, student_id, hours):
        self.student_id = student_id
        self.hours = hours