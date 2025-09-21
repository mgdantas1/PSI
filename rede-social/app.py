from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secreto'

login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager.__init__(app)

db = SQLAlchemy()

db.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False)
    senha = db.Column(db.String(15), nullable=False)

    posts = db.relationship('Post', backref='user')
    comentarios = db.relationship('Comentario', backref='user')

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conteudo = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comentarios = db.relationship('Comentario', backref='post')


class Comentario(db.Model):
    __tablename__ = 'comentario'

    comentario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ROTAS

@app.route('/')
def index():
    posts = Post.query.all()
    if posts:
        return render_template('index.html', posts=posts)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        senha = request.form['senha']
        senha_h = generate_password_hash(senha)

        verificar = User.query.filter_by(username=username).first()

        if not verificar:
            novo_user = User(username=username, email=email, senha=senha_h)
            db.session.add(novo_user)
            db.session.commit()

            login_user(novo_user)
            
            flash('Usuário cadastrado com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Usuário já cadastrado!', category='error')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            flash('Usuário logado com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Dados incorretos!', category='error')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        conteudo = request.form['post']
        db.session.add(Post(conteudo=conteudo, user_id=user.id))
        db.session.commit()

        flash('Post carregado com sucesso!', category='success')
        return redirect(url_for('index'))
    
    return render_template('new_post.html', user=user)

@login_required
@app.route('/posts')
def posts():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('posts.html', posts=posts)

@login_required
@app.route('/comentarios')
def comentarios():
    post_id = request.args.get('id')
    comentarios = Comentario.query.filter_by(post_id=post_id).all()
    return render_template('comentarios.html', comentarios=comentarios)

@login_required
@app.route('/novo_coment', methods=['POST'])
def novo_coment():
    texto = request.form['coment']
    post_id = request.args.get('id')
    db.session.add(Comentario(texto=texto, user_id=current_user.id, post_id=post_id))
    db.session.commit()

    flash('Novo comentário adicionado com sucesso!', category='success')
    return redirect(url_for('comentarios', id=post_id))

@login_required
@app.route('/remover_coment')
def remover_coment():
    coment_id = request.args.get('coment_id')
    comentario = Comentario.query.get(coment_id)
    db.session.delete(comentario)
    db.session.commit()

    flash('Comentário excluido...', category='success')
    return redirect(url_for('comentarios', id=comentario.post_id))

@login_required
@app.route('/editar_coment', methods=['GET', 'POST'])
def editar_coment():
    coment_id = request.args.get('coment_id')
    comentario = Comentario.query.get(coment_id)
    if request.method == 'POST':
        coment = request.form['novo_comentario']
        comentario.texto = coment
        db.session.commit()

        flash('Nova atualização salva...', category='success')
        return redirect(url_for('comentarios', id=comentario.post_id))
    
    return redirect(url_for('comentarios', editar='editar', id=comentario.post_id))