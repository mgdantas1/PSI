from flask import Flask, render_template
from flask import request, session, redirect, url_for
from flask import flash

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, UserMixin, logout_user, current_user
from flask_login import login_required, login_user

import sqlite3

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = 'chave_secreta'

def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self, nome, senha) -> None:
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao() 
        sql = "select * from users where nome = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        user = User(nome=resultado['nome'], senha=resultado['senha'])
        user.id = resultado['nome']
        return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']
        
        conexao = obter_conexao()
        sql = "select * from users where nome = ? and senha = ?"
        resultado = conexao.execute(sql, (nome, senha)).fetchone()
        if resultado:
            ## verdade
            user = User(nome=resultado['nome'], senha=resultado['senha'])
            user.id = nome
            login_user(user)
            return redirect(url_for('dash'))

        flash('Dados incorretos', category='error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']

        # obter uma conexão
        conexao = obter_conexao() 
        # nome é a coluna "NOME" e o "?" é o valor que vai ser substituido pelo variável nome ("nome,")
        sql = "select * from users where nome = ?"
        # fetchone recupera o dado da consulta
        resultado = conexao.execute(sql, (nome,)).fetchone()
        print(resultado)
        if not resultado:
            sql = "INSERT INTO users(nome, senha) VALUES (?, ?)"
            conexao.execute(sql, (nome, senha))
            conexao.commit()
            user = User(nome=nome, senha=senha)
            user.id = nome
            login_user(user)
            # flash('Cadastro realizado com sucesso!', category='error')
            return redirect(url_for('dash'))

        conexao.close()
        flash('Problema no cadastro', category='error')
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/festa', methods=['GET', 'POST'])
@login_required
def festa():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        usuario = current_user.id
        conn = obter_conexao()
        buscar_id = "SELECT * FROM users WHERE NOME = ?"
        resultado = conn.execute(buscar_id, (usuario,)).fetchone()
        if resultado:
            usuario_id = resultado['id']
        sql = "INSERT INTO festas(nome, valor, user_id) VALUES (?, ?, ?)"
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(sql, (nome, valor, usuario_id))
        conn.commit()
        conn.close()
        flash(f'Festa inserida com sucesso. Dados: {nome} - R${valor}', category='success')
        return redirect(url_for('index'))
    return render_template('formulario_festa.html')

@app.route('/dashboard')
@login_required
def dash():
    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))