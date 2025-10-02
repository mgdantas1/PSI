import sqlite3

# estabelecer uma conexão
# -- "banco.db" é o database
conexao = sqlite3.connect("banco.db")

# executar instrução de criação de tabelas
# abre o arquivo e o lê
with open('schema.sql') as f:
    # manda a conexão executar como script
    conexao.executescript(f.read())
    # -- passa o arquivo e a lista de usuários
    # conexao.executemany(f.read(), lista)

# fechar conexão
conexao.close()


