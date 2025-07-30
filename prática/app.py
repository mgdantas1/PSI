import sqlite3

from criar_banco import criar_banco

from flask import Flask, flash, redirect, request, render_template, url_for, session

from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()

criar_banco()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = 'secreto'


def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self, nome: str, senha: str, email: str):
        self.nome = nome
        self.senha = senha
        self.email = email

    @classmethod
    def get(cls, user_id):
        conn = obter_conexao()
        sql = 'select * from users where id = ?'
        res = conn.execute(sql, (user_id, )).fetchone()
        if res:
            user = User(nome = res['nome'], senha = res['senha'], email = res['email'])
            user.id = user_id
            return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        senha = generate_password_hash(senha)
        email = request.form['email']

        conn = obter_conexao()
        sql = 'SELECT * FROM users WHERE email = ?'
        res = conn.execute(sql, (email, )).fetchone()
        if not res:
            sql = 'INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)'
            conn.execute(sql, (nome, email, senha))
            conn.commit()
            user = User(nome = nome, email = email, senha = senha)
            cont = conn.execute('SELECT COUNT(*) FROM users').fetchone()
            id = cont[0]
            user = User(nome=nome, email=email, senha=senha)
            user.id = id
            login_user(user)
            return redirect(url_for('index'))
        conn.close()
        # flash
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = obter_conexao()

        sql = 'SELECT * FROM users WHERE email = ?'
        res = conn.execute(sql, (email, )).fetchone()
        if res:
            id = res['id']
            nome = res['nome']
            senha_h = res['senha']
            if check_password_hash(senha_h, senha):
                user = User(nome=nome, email=email, senha=senha_h)
                user.id = id
                login_user(user)
                return redirect(url_for('index'))
            return redirect(url_for('login'))
        # flash
        return redirect(url_for('login'))
    return render_template('login.html')