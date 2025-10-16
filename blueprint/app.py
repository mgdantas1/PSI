from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import *
from users.user import user_bp
from books.books import book_bp
from main.index import main_bp


app = Flask(__name__)
app.secret_key = 'secreto'

app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(main_bp)

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        return session.get(User, int(user_id))
    
