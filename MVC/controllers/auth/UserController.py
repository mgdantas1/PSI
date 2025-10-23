from flask import Blueprint, request
from flask_login import login_user
from models.users import User
from database import engine
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

user_bp = Blueprint('users', __name__)
    
@user_bp.route('/register')
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()

            if not user:
                senha_c = generate_password_hash(senha)
                new_user = User(email=email, senha=senha)
                session.add(new_user)
                login_user(new_user)
                session.commit()

                return 'ok'
            
            return 'já existe'
    
    return 'register'
