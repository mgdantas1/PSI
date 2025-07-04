from flask import Flask, render_template, request, \
    make_response, redirect, url_for, session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'segredodificil'

@app.route('/')
def index():
    return render_template('index.html')
    # retornar response

@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('cadastro.html')
    else:
        # 'nome' é o atributo 'name' do input
        nome = request.form['nome']
        genero = request.form['genero']

        # guardar o usuário na sessão
        session['user'] = nome
        
        response = make_response(
            redirect(  url_for('preferencia')  ))
        response.set_cookie(nome, genero, max_age=7*24*3600) 
        
        return response
        

@app.route('/preferencia')
def preferencia():

    if 'user' in session:
        user = session.get('user')
        if user in request.cookies:
            genero = request.cookies.get(user)
            return user + " - " + genero

    return "<h1>Deu ruim</h1>"

@app.route('/recomendar')
def recomendar():
    filmes = {
        'acao' : ['tiro, porrada e boma', 'estudar', 'prova-psi'],
        'comedia' : ['vale ponto?', 'a prova é escrita?', 
            'hoje vou liberar mais cedo'],
        'drama' : ['X', 'Y', 'Z'],
        'sifi' : ['coding', 'the coding', 'the code coding'], 
    }
    if 'genero' not in request.args:
        return 'GENERO não informado'
    genero = request.args.get('genero')
    if genero in filmes.keys():
        lista = filmes[genero]

    return render_template('filmes.html', filmes=lista)
