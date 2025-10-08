from models import *
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secreto'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        return session.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()

            if not user:
                senha_g = generate_password_hash(senha)
                new_user = User(email=email, senha=senha_g)
                session.add(new_user)
                session.commit()

                login_user(new_user)


                flash('Usuário cadastrado com sucesso!', category='success')
                return redirect(url_for('index'))

        flash('Usuário já possui cadastro!', category='error')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            user = session.query(User).filter_by(email=email).first()

            if user and check_password_hash(user.senha, senha):
                login_user(user)

                flash('Login realizado com sucesso!', category='success')
                return redirect(url_for('index'))
        
        flash('Dados incorretos!', category='error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        texto = request.form['texto']
        user_id = current_user.id

        new_task = Tarefa(tarefa=texto, user_id=user_id)

        with Session(bind=engine) as session:
            session.add(new_task)
            session.commit()


        flash('Tarefa adicionada com sucesso', category='success')
        return redirect(url_for('tasks'))
    
    return render_template('new_tasks.html')

@app.route('/tasks')
@login_required
def tasks():
    user_id = current_user.id

    with Session(bind=engine) as session:
        user = session.get(User, user_id)

        tasks = user.tarefas


    return render_template('tasks.html', tarefas=tasks)

@app.route('/edit_task', methods=['GET', 'POST'])
def edit_task():
    task_id = request.args['task_id']
    if request.method == 'POST':
        texto = request.form['texto']

        task_id = request.args['task_id']

        with Session(bind=engine) as session:
            task = session.query(Tarefa).filter_by(id=task_id).first()

            task.tarefa = texto

            session.commit()

        flash('Tarefa alterada com sucesso!', category='success')
        return redirect(url_for('tasks'))
    
    return render_template('edit_tasks.html', task_id=task_id)

@app.route('/delete_task')
@login_required
def delete_task():
    task_id = request.args['task_id']
    
    with Session(bind=engine) as session:
        task = session.get(Tarefa, task_id)

        session.delete(task)
        session.commit()

    flash('Tarefa deletada!', category='success')
    return redirect(url_for('tasks'))

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))