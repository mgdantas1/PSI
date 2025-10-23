from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.users import User
from sqlalchemy.orm import Session

from app import app, engine

from flask import request

app.secret_key = 'secreto'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        return session.get(User, int(user_id))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass