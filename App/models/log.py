from App.database import db

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

    student = db.relationship("Student", backref='log')
    staff = db.relationship("Staff", backref='log')
    activity = db.relationship("Activity", backref='log')

    def __init__(self, staff_id, student_id, activity_id, hours):
        self.staff_id = staff_id
        self.student_id = student_id
        self.hours = hours
        self.activity_id = activity_id
    
    def get_json(self):
        return{
            'id': self.id,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'hours': self.hours
        }