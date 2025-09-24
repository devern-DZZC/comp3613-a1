from App.models import db, Activity

def create_activity(name):
    activity = Activity(name)
    db.session.add(activity)
    db.session.commit()


MILESTONES = [10, 25, 50]
ACTIVITY_MILESTONES = {}

def milestones_for(activity_name):
    return ACTIVITY_MILESTONES.get(activity_name, MILESTONES)

def resolve_milestone(total_hours, milestones):
    milestones = sorted(milestones)
    reached = None
    for nextt in milestones:
        if total_hours >= nextt:
            reached = nextt
    result = f"{reached} Hour Milestone" if reached is not None else "No milestone yet"
    return result
