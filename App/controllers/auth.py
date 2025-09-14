from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request, unset_jwt_cookies
import json, os
from App.models import User
from App.database import db

SESSION_FILE = "cli_session.json"

def get_current_user():
   if not os.path.exists(SESSION_FILE):
      return None
   with open(SESSION_FILE) as f:
      data = json.load(f)
      user = User.query.get(data['user_id'])
      return user

def login(username, password):
  user = User.query.filter_by(username=username).first()
  if not user or not user.check_password(password):
     print('User not found or incorrect password')
     return False
  with open(SESSION_FILE, 'w') as f:
     json.dump({"user_id": user.id, "user_type": user.type}, f)
  print(f"Logged in as: {user.username} ({user.type})")
  return True


def logout():
  if os.path.exists(SESSION_FILE):
     os.remove(SESSION_FILE)
     print("Logged out")
  else:
     print("Not logged in. Please log in.")


def setup_jwt(app):
  jwt = JWTManager(app)

  # Always store a string user id in the JWT identity (sub),
  # whether a User object or a raw id is passed.
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user_id = getattr(identity, "id", identity)
    return str(user_id) if user_id is not None else None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    # Cast back to int primary key
    try:
      user_id = int(identity)
    except (TypeError, ValueError):
      return None
    return db.session.get(User, user_id)

  return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          identity = get_jwt_identity()
          user_id = int(identity) if identity is not None else None
          current_user = db.session.get(User, user_id) if user_id is not None else None
          is_authenticated = current_user is not None
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)