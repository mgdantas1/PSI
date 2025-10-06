from models import *
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secreto'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = session.query(User).filter_by(email=email).first()

        if not user:
            senha_g = generate_password_hash(senha)
            new_user = User(email=email, senha=senha_g)
            session.add(new_user)
            session.commit()

            login_user(new_user)

            session.close()

            return redirect(url_for('index'))



        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))