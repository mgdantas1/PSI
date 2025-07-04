from flask_login import UserMixin, login_manager, login_required, logout_user, login_user, LoginManager, current_user
from flask import session
import json

class User(UserMixin):
    id_user = None
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        usuarios = session['usuarios']
        for id, dados in usuarios.items():
            if user_id == id:
                user = User(nome = dados['nome'], senha = dados['senha'])
                user.id = user_id
                return user


    @classmethod
    def load(cls, arq):
        with open(arq) as file:
            return json.load(file)
        
    @classmethod
    def write(cls, dicio, arq):
        with open(arq, 'w') as file:
            return json.dump(dicio, file)