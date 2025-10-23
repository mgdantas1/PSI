from flask import Blueprint
from database import *
from app import *


user_bp = Blueprint('users', __name__, template_folder='templates')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()

            if not user:
                senha_h = generate_password_hash(senha)
                new_user = User(email=email, senha=senha_h)
                session.add(new_user)
                session.commit()
                login_user(new_user)
                flash('Usuário registrado com sucesso!', category='success')
                return redirect(url_for('main.index'))
            
            flash('Email já existe!', category='error')
            return redirect(url_for('users.login'))

    return render_template('register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.senha, senha):
                login_user(user)
                return redirect(url_for('main.index'))
            flash('Dados incorretos', category='success')
    return render_template('login.html')
