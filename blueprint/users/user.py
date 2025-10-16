from flask import Blueprint
from database import *
from app import *


user_bp = Blueprint('users', __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()

            if user:
                flash('Email já cadastrado!')
                return redirect(url_for('register'))

            new_user = User(nome=nome, email=email, senha=senha)
            session.add(new_user)
            session.commit()
            login_user(new_user)
            flash('Usuário registrado com sucesso!')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user_data = session.query(User).filter_by(email=email).first()
            if user_data and senha == user_data.senha:
                login_user(user_data)
                return redirect(url_for('profile'))
            flash('Credenciais inválidas!')
    return render_template('login.html')
