from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import session
import json

class User(UserMixin):
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        usuarios = session['usuarios']
        if user_id in usuarios:
            user = User(nome=usuarios[user_id]['nome'], senha=usuarios[user_id]['senha'])
            user.id = user_id
            return user
        
    @classmethod
    def load(cls, arq):
        if arq:
            with open(arq) as file:
                return json.load(file)
        
    @classmethod
    def write(cls, arq, dicio):
        with open(arq, 'w') as file:
            return json.dump(dicio, file)