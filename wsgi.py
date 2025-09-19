import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Student, Staff, Log, Request
from App.main import create_app
from App.controllers import ( create_user, create_staff ,get_all_users_json, get_all_users, initialize, login, logout, 
                             get_current_user, get_all_logs, get_all_logs_json )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

def require_role(role):
    def decorator(func):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            user = get_current_user()
            if not user:
                raise click.ClickException("Not logged in.")
            if user.type != role:
                raise click.ClickException(f'Not logged in as {role}. Cannot perform this function.')
            return ctx.invoke(func, *args, **kwargs, current_user=get_current_user())
        return wrapper
    return decorator

def add_student_hours(student_id, hours):
    student = Student.query.get(student_id)
    if student:
        currentHours = student.hours
        newHours = currentHours + hours
        student.set_hours(newHours)
        db.session.add(student)
        db.session.commit()

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

@app.cli.command("leaderboard", help="Shows the Leaderboard")
def view_leaderboard():
    students = (Student.query
                .order_by(Student.hours.desc(), Student.username.asc())
                .all())
    
    if not students:
        print('No students added.')
        return
    print('=====LEADERBOARD=====')
    for i, student in enumerate(students):
        print(f'{i+1}. {student.username}: {student.hours} Hours')
    

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("user_type", default="student")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(user_type, username, password):
    if user_type == "student":
        create_user(username, password)
    elif user_type == 'staff':
        create_staff(username, password)
    else:
        print('Command not recognized. Try flask user create <user_type> <username> <password>')
        return
    user = User.query.filter_by(username=username).first()
    print(f'Created {user_type}: {username} (id = {user.id})')

# this command will be : flask user create student bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@user_cli.command("logs", help="Lists logs in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_logs())
    else:
        print(get_all_logs_json())

@user_cli.command("requests", help="Lists requests in the database")
@require_role("staff")
def view_all_requests(current_user):
    requests = Request.query.all()
    if not requests:
        print('No requests found.')
        return
    print("REQUEST ID   STUDENT NAME    REQUESTED HOURS")
    for request in requests:
        student = Student.query.get(request.student_id)
        print(f"{request.id}            {student.username}             {request.hours}")


@user_cli.command("login", help="Logs in the user")
@click.argument("username", type=str)
@click.argument("password", type=str)
def login_user(username, password):
    login(username, password)

@user_cli.command("logout", help="Log out current user")
def logout_user():
    logout()

@user_cli.command("log", help="Logs hours for student")
@click.argument("username", type=str)
@click.argument("hours", type=int)
@require_role("staff")
def log_hours(username, hours, current_user):
    student = Student.query.filter_by(username=username).first()
    if student:
        log = Log(staff_id=current_user.id, student_id=student.id, hours=hours)
        db.session.add(log)
        add_student_hours(student_id=student.id, hours=hours)
        print(f"Logged {hours} hours for {username} successfully.")
        print(f"{student.username}'s Total Hours: {student.hours} Hours")
        return
    print("User does not exist.")

@user_cli.command("accolades", help="View milestone accolades")
@require_role("student")
def view_accolades(current_user):
    user = get_current_user()
    student = Student.query.get(user.id)
    if student:
        if student.hours < 10:
            print('No milestone reached yet.')
        elif student.hours >= 10 and student.hours < 25:
            student.accolade = "10 Hour Milestone"
        elif student.hours >= 25 and student.hours < 50:
            student.accolade = "25 Hour Milestone"
        elif student.hours >= 50:
            student.accolade = "50 Hour Milestone"
        print(f"{student.username}'s Accolade: {student.accolade}")
    else:
        print('Student not found.')


app.cli.add_command(user_cli) # add the group to the cli

@user_cli.command("request", help="Allows a student to request hours")
@click.argument("hours", type=int)
@require_role("student")
def request_hours(hours, current_user):
    student = Student.query.get(current_user.id)
    if student:
        request = Request(student_id=current_user.id, hours=hours)
        db.session.add(request)
        db.session.commit()
        print(f"{student.username} requested {hours} hours.")
    else:
        print('Student not found.')

@user_cli.command("confirm", help="Approve/Reject requested hours")
@click.argument("action", type=str)
@click.argument("request_id", type=int)
@require_role("staff")
def confirm_hours(action, request_id, current_user):
    request = Request.query.get(request_id)
    if request:
        student = Student.query.get(request.student_id)
        if action == "approve":
            log = Log(staff_id=current_user.id, student_id=request.student_id, hours=request.hours)
            add_student_hours(student_id=student.id, hours=request.hours)
            db.session.add(log)
            db.session.delete(request)
            db.session.commit()
            print(f"{request.hours} hours approved for {student.username}")
        elif action == "reject":
            db.session.delete(request)
            db.session.commit()
            print(f"{request.hours} hours rejected for {student.username}")
        else:
            print("Wrong action entered. Please enter 'approve' or 'reject' followed by the request_id")
    else:
        print('Request not found.')

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)