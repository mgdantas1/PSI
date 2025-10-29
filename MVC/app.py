from flask import Flask, render_template
from flask_login import LoginManager
from sqlalchemy.orm import Session
from database import User, engine
from controllers.auth.UserController import user_bp
from controllers.ProductsController import product_bp

app = Flask(__name__)

app.secret_key = 'secreto'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        return session.get(User, str(user_id))

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)