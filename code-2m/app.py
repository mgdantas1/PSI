from flask import Flask, render_template, request, session, redirect, url_for
from models import User, login_manager, login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)

login_manager = LoginManager()

login_manager.init_app(app)

app.config['SECRET_KEY'] = 'RANCA TAMPA E MANDA BOI'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'usuarios' not in session:
        User.write({}, 'compras.json')
        session['usuarios'] = {}
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        for id, dados in session['usuarios'].items():
            if nome == dados['nome'] and check_password_hash(dados['senha'], senha):
                user = User(nome=nome, senha=senha)
                user.id = id
                login_user(user)
                return redirect(url_for('produtos'))
            
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        senha_c = generate_password_hash(senha)

        for dados in session['usuarios'].values():
            if nome in dados.values():
                return redirect(url_for('login'))

        user_id = str(len(session['usuarios']) + 1)
        session['usuarios'][user_id] = {'nome': nome, 'senha': senha_c}
        user = User(nome=nome, senha=senha_c)
        user.id = user_id
        login_user(user)
        session['logout'] = True
        return redirect(url_for('produtos'))

    return render_template('cadastro.html')

@login_required
@app.route('/produtos')
def produtos():
    produtos = User.load('produtos.json')
    return render_template('produtos.html', produtos=produtos)


@login_required
@app.route('/adicionar', methods=['POST'])
def adicionar():
    compras = User.load('compras.json')
    id = current_user.id
    if id not in compras:
        compras[id] = {
            'itens': {},
            'total': 0
        }
    if request.method == 'POST':
        prod = request.form['prod']
        
        produtos = User.load('produtos.json')

        print(compras)

        if prod in compras[id]['itens']:
            compras[id]['itens'][prod] += 1
        else:
            compras[id]['itens'][prod] = 1
        
        soma = 0
        for prod, quant in compras[id]['itens'].items():
            soma += produtos[prod] * quant

        compras[id]['total'] = soma

        User.write(compras, 'compras.json')

        return redirect(url_for('carrinho'))

        

@login_required
@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    compras = User.load('compras.json')
    id = current_user.id
    carrinho = compras[id]
    valor = carrinho['total']
    if request.method == 'POST':
        valor = 0
        carrinho['itens'] = {}
        carrinho['total'] = 0
        User.write(compras, 'compras.json')
        return render_template('cadastro.html', valor = valor)

    return render_template('carrinho.html', carrinho = carrinho, valor = valor)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

