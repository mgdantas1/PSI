from flask import Flask, redirect, request, render_template, url_for, flash

import sqlite3

app = Flask(__name__)

def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']

        conn = obter_conexao()
        sql = 'INSERT INTO users (nome) VALUES (?)'
        conn.execute(sql, (nome, ))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    conn = obter_conexao()
    sql = 'SELECT * FROM users'
    lista = conn.execute(sql).fetchall()
    conn.close()
    # reenviar

    return render_template('index.html', lista = lista)