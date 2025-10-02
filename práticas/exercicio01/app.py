from models import *
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'secreto'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_g = generate_password_hash(senha)

        session.begin()

        query = session.query(User).filter_by(nome=nome).first()

        if not query:
            user = User(nome=nome, email=email, senha=senha_g)
            login_user(user)
            session.add(user)
            session.commit()
            session.close()

            flash('Usuário cadastrado com sucesso!', category='success')
            return redirect(url_for('index'))
    
    flash('Usuário já possui cadastro!', category='error')
    return render_template('register.html')
