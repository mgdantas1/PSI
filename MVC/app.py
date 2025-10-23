from flask import Flask
from flask_login import LoginManager
from sqlalchemy.orm import Session
from database import Base, User, engine
from controllers.auth.UserController import user_bp

app = Flask(__name__)

app.secret_key = 'secreto'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        return session.get(User, int(user_id))

app.register_blueprint(user_bp)

@app.route('/')
def index():
    return 'página inicial'