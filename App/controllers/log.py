from App.models import Log
from App.database import db


def get_all_logs():
    return db.session.scalars(db.select(Log)).all()

def get_all_logs_json():
    logs = get_all_logs()
    if not logs:
        return []
    logs = [log.get_json() for log in logs]
    return logs

def create_log():
    return