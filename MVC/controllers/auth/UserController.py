from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.users import User
from database import engine
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('users', __name__)
    
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()

            if not user:
                senha_c = generate_password_hash(senha)
                new_user = User(email=email, senha=senha_c)
                session.add(new_user)
                session.commit()
                login_user(new_user)

                flash('Cadastro realizado com sucesso!', category='success')
                return redirect(url_for('index'))
            
            flash('Usuário já cadastrado!', category='error')
            return redirect(url_for('users.login'))
    
    return render_template('user/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()

            if user and check_password_hash(user.senha, senha):
                login_user(user)
                
                flash('Login realizado com sucesso!', category='success')
                return redirect(url_for('index'))
            
            flash('Dados incorreto!', category='error')
            return redirect(url_for('users.login'))
        
    return render_template('user/login.html')


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))