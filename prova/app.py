from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

app.secret_key = 'secreto'

def conexao():
    conn = sqlite3.connect('banco.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        senha = request.form['senha']

        conn = conexao()
        verificar = 'SELECT * FROM users WHERE matricula = ?'
        res = conn.execute(verificar, (matricula, )).fetchone()
        if not res:
            sql = 'INSERT INTO users (nome, matricula, senha) VALUES (?, ?, ?)'
            conn.execute(sql, (nome, matricula, senha))
            conn.commit()
            conn.close()
            return redirect(url_for('index.html'))
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/register_peca', methods=['GET', 'POST'])
def register_peca():
    if request.method == 'POST':
        nome = request.form['nome']
        turma = request.form['turma']

        conn = conexao()
        verificar = 'SELECT * FROM pecas WHERE nome = ?'
        res = conn.execute(verificar, (nome, )).fetchone()
        if not res:
            sql = 'INSERT INTO pecas (nome, turma) VALUES (?, ?)'
            conn.execute(sql, (nome, turma))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        return redirect(url_for('register_peca'))
    return render_template('register_peça.html')

@app.route('/procurar_peca', methods=['GET', 'POST'])
def procurar_peca():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = conexao()
        sql = 'SELECT * FROM pecas WHERE nome = ?'
        lista = conn.execute(sql, (nome, )).fetchall()
        conn.close()
        if lista:
            return render_template('peça.html', lista=lista)
        return redirect(url_for('procurar_peca'))
    return render_template('procurar_peça.html')

@app.route('/exibir_peca')
def exibir_peca():
    nome = request.args.get('nome')
    turma = request.args.get('turma')
    if nome == None:
        peca = {
            'nome': nome,
            'turma': turma
        }
    else:
        peca = None
    return render_template('peça.html', peca=peca)

@app.route('/exibir_pecas')
def exibir_pecas():
    conn = conexao()
    lista = conn.execute(f'SELECT * FROM pecas').fetchall()
    conn.close()
    return render_template('peças.html', lista=lista)

@app.route('/remover_peca')
def remover_peca():
    nome = request.args.get('nome')
    conn = conexao()
    sql = 'DELETE FROM pecas WHERE nome = ?'
    conn.execute(sql, (nome, )) 
    conn.commit()
    conn.close()

    return redirect(url_for('exibir_pecas'))

@app.route('/user')
def user():
    nome = request.args.get('nome')
    matricula = request.args.get('matricula')
    user = {'nome': nome, 'matricula': matricula}
    return render_template('user.html', user=user)

@app.route('/usuarios')
def usuarios():
    conn = conexao()
    lista = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('usuarios.html', lista = lista)

@app.route('/register_danca', methods=['GET', 'POST'])
def register_danca():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']

        conn = conexao()
        verificar = 'SELECT * FROM dancas WHERE matricula = ?'
        res = conn.execute(verificar, (matricula, )).fetchone()
        if not res:
            sql = 'SELECT * FROM users WHERE matricula = ?'
            id = conn.execute(sql, (matricula, )).fetchone()
            if id:
                user_id = id['id']
                sql = 'INSERT INTO dancas (nome, matricula, user_id) VALUES (?, ?, ?)'
                conn.execute(sql, (nome, matricula, user_id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
            return redirect(url_for('register_danca'))
        return redirect(url_for('register_danca'))
    return render_template('register_dança.html')

@app.route('/update_peca', methods=['GET', 'POST'])
def update_peca():
    conn = conexao()
    peca = conn.execute('SELECT * FROM pecas').fetchall()
    if peca:
        if request.method == 'POST':
            nome = request.form['nome']
            turma = request.form['turma']
            id = request.form['peca']
            sql = 'UPDATE pecas SET nome = ?, turma = ? WHERE id = ?'
            conn.execute(sql, (nome, turma, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        return render_template('update_peca.html', peca=peca)
    return render_template('index.html')

@app.route('/exibir_dancas')
def exibir_dancas():
    conn = conexao()
    lista = conn.execute(f'SELECT * FROM dancas').fetchall()
    conn.close()
    return render_template('danças.html', lista=lista)

@app.route('/exibir_danca')
def exibir_danca():
    nome = request.args.get('nome')
    matricula = request.args.get('matricula')

    if nome == None:
        danca = {
            'nome': nome,
            'matricula': matricula
        }
    else:
        danca = None

    return render_template('dança.html', danca=danca)

@app.route('/procurar_danca', methods=['GET', 'POST'])
def procurar_danca():
    if request.method == 'POST':
        id = request.form['id']
        conn = conexao()
        sql = 'SELECT * FROM dancas WHERE id = ?'
        res = conn.execute(sql, (id, )).fetchall()
        if res:
            return render_template('procurar_dança.html', lista=res)
        return redirect(url_for('procurar_danca'))
    return render_template('procurar_dança.html')