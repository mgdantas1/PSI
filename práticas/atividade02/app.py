from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'secreto'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    curso = db.Column(db.String(100), nullable=False, unique=True)
    # vai servir como um atalho para poder acessar direto o curso ao qual o aluno pertence
    aluno = db.relationship('Aluno', backref='curso')

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    # chave estrangeira
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)



# criando as tabelas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    alunos = {}
    
    tb_aluno = Aluno.query.all()
    for dados in tb_aluno:
        novo_aluno = {}
        novo_aluno['nome'] = dados.nome
        novo_aluno['email'] = dados.email
        curso = dados.curso.curso
        novo_aluno['curso'] = curso
        alunos[dados.id] = novo_aluno
    print(alunos)
    return render_template('index.html', alunos=alunos)

@app.route('/novo_curso', methods=['GET', 'POST'])
def novo_curso():
    if request.method == 'POST':
        curso = (request.form['curso']).strip().upper()
        
        verificar_curso = Curso.query.filter_by(curso=curso).first()
        if not verificar_curso:
            novo_curso = Curso(curso=curso)
            db.session.add(novo_curso)
            db.session.commit()
            flash('Curso cadastrado com sucesso', category='success')
            return redirect(url_for('index'))
        flash('Curso já cadastrado', category='error')
        return redirect(url_for('novo_curso'))
    return render_template('curso.html')

@app.route('/novo_aluno', methods=['GET', 'POST'])
def novo_aluno():
    
    cursos = Curso.query.all()
    if cursos:
        if request.method == 'POST':
            nome = request.form['nome']
            email = (request.form['email']).strip().lower()
            curso = request.form['cursos']

            verificar_email = Aluno.query.filter_by(email=email).first()

            if not verificar_email:
                cursos = Curso.query.filter_by(curso=curso).first()
                novo_aluno = Aluno(nome=nome, email=email, curso_id=cursos.id)
                db.session.add(novo_aluno)
                db.session.commit()
                
                flash('Aluno cadastrado com sucesso', category='success')
                return redirect(url_for('index'))
            
            
            flash('Aluno já cadastrado', category='error')
            return redirect(url_for('novo_aluno'))

        return render_template('aluno.html', cursos=cursos)
    
    flash('Ainda não há cursos cadastrados', category='error')
    return redirect(url_for('index'))

@app.route('/editar', methods=['GET', 'POST'])
def editar():
    
    cursos = Curso.query.all()
    if cursos:
        if request.method == 'POST':
            email = request.form['email'].strip().lower()
            curso_novo = request.form['cursos']
            
            aluno = Aluno.query.filter_by(email=email).first()
            curso_antigo = Curso.query.filter_by(curso=curso_novo).first()

            if aluno:
                aluno.curso_id = curso_antigo.id
                db.session.commit()
                

                flash('Curso atualizado com sucesso', category='success')
                return redirect(url_for('index'))
        
            
            flash('O email pode estar incorreto', category='error')
            return redirect(url_for('editar'))

        return render_template('editar.html', cursos=cursos)
    
    flash('Ainda não há cursos cadastrados', category='error')
    return redirect(url_for('index'))

@app.route('/remover', methods=['GET', 'POST'])
def remover():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()

        

        aluno = Aluno.query.filter_by(email=email).first()

        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            

            flash('Aluno removido com sucesso', category='success')
            return redirect(url_for('index'))
        
        
        flash('O email pode estar incorreto', category='error')
        return redirect(url_for('editar'))
    
    return render_template('editar.html')

    