from flask import Flask, render_template, request, make_response, url_for, session, redirect, flash
from models import LoginManager, login_required, login_user, logout_user, User, current_user
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = 'chave_secreta'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'usuarios' not in session:
        session['usuarios'] = {}
        User.write('votos.json', {})
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        senha = generate_password_hash(senha)

        usuarios = session['usuarios']
        for dados in usuarios.values():
            if nome == dados['nome']:
                flash('Usuário já cadastrado', category="error")
                return redirect(url_for('cadastro'))
            
        id = str(len(usuarios) + 1)
        usuarios[id] = {'nome': nome, 'senha': senha}
        session['usuarios'] = usuarios

        user = User(nome=nome, senha=senha)
        user.id = id
        login_user(user)

        response = make_response(redirect(url_for('votacao')))
        response.set_cookie('nome', nome)
        return response
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        usuarios = session['usuarios']
        for id, dados in usuarios.items():
            if nome == dados['nome'] and check_password_hash(dados['senha'], senha):
                user = User(nome=nome, senha=dados['senha'])
                user.id = id
                login_user(user)
                response = make_response(redirect(url_for('votacao')))
                response.set_cookie('nome', nome)

                return response
        flash('Usuário ou senha incorretos', category='error')
        return redirect(url_for('login'))    
        
    return render_template('login.html')

@login_required
@app.route('/votacao', methods=['GET', 'POST'])
def votacao():
    opcoes = User.load('opcoes.json')
    if request.method == 'POST':
        opcao = request.form['opcao']
        id = current_user.id
        arq = User.load('votos.json')
        if id in arq:
            flash('O usuário já votou.', category='error')
            return redirect(url_for('votacao'))
        arq[id] = opcao
        User.write('votos.json', arq)
        return render_template('agradecimento.html')
    return render_template('votacao.html', opcoes=opcoes)

@login_required
@app.route('/agradecimento')
def agradecimento():
    return render_template('agradecimento.html')

@login_required
@app.route('/resultados')
def resultados():
    arq = User.load('votos.json')
    dicio = {}
    for valor in arq.values():
        if valor not in dicio:
            dicio[valor] = 1
        else:
            dicio[valor] += 1
    return render_template('resultados.html', votos=dicio)
    

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))