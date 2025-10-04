from models import *
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'secreto'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        user_id = current_user.id
        user = session.query(User).get(user_id)
        times = user.times
        return render_template('index.html', times=times)
    return render_template('index.html', times=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_g = generate_password_hash(senha)


        query_user = session.query(User).filter_by(email=email).first()

        if not query_user:
            user = User(nome=nome, email=email, senha=senha_g)
            session.add(user)
            session.commit()
            login_user(user)

            flash('Usuário cadastrado com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Usuário já possui cadastro!', category='error')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        query_user = session.query(User).filter_by(email=email).first()

        if query_user and check_password_hash(query_user.senha, senha):
            login_user(query_user)
            flash('Usuário logado com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Dados incorretos!', category='error')
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/register_time', methods=['GET', 'POST'])
@login_required
def register_time():
    if request.method == 'POST':
        nome = request.form['nome']

        query_time = session.query(Time).filter_by(nome=nome).first()

        if not query_time:
            time = Time(nome=nome)
            session.add(time)
            session.commit()

            flash('Time cadastrado com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Time já cadastrado!', category='error')
        return redirect(url_for('register_time'))
    
    return render_template('register_time.html')

@app.route('/option_time', methods=['GET', 'POST'])
def option_time():
    times = session.query(Time).all()
    if request.method == 'POST':
        opcao = int(request.form['opcao'])
        user_id = current_user.id
        user = session.query(User).filter_by(id=user_id).first()
        time = session.query(Time).get(opcao)

        if time not in user.times:
            user.times.append(time)
            session.commit()
            flash('Time definido com sucesso!', category='success')
            return redirect(url_for('index'))

        flash('O usuário já possui o time!', category='error')
        return redirect(url_for('option_time'))

    return render_template('option_time.html', times=times)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))