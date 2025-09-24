from App.database import db

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name