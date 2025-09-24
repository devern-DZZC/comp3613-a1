from App.database import db

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    hours = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student", backref='request')
    activity = db.relationship("Activity", backref='request')

    def __init__(self, student_id, activity_id, hours):
        self.student_id = student_id
        self.activity_id = activity_id
        self.hours = hours