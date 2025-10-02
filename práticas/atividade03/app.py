from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = 'secreto'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

class Professor(db.Model):
    __tablename__ = 'professor'

    pro_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pro_nome = db.Column(db.String(150), nullable=False, unique=True)
    pro_email = db.Column(db.String(150), nullable=False, unique=True)

    disciplina = db.relationship('Disciplina', backref='professor')

disciplina_aluno = db.Table('disciplina_aluno',
    db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplina.dis_id'), primary_key=True),
    db.Column('aluno_id', db.Integer, db.ForeignKey('aluno.alu_id'), primary_key=True)
)

class Disciplina(db.Model):
    __tablename__ = 'disciplina'

    dis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dis_nome = db.Column(db.String(50), nullable=False, unique=True)
    dis_pro_id = db.Column(db.Integer, db.ForeignKey('professor.pro_id'), nullable=False)

class Aluno(db.Model):
    __tablename__ = 'aluno'

    alu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alu_nome = db.Column(db.String(150), nullable=False)
    alu_email = db.Column(db.String(150), nullable=False, unique=True)

    disciplina = db.relationship('Disciplina', secondary='disciplina_aluno', backref='aluno')

with app.app_context():
    db.create_all()


# rotas

@app.route('/')
def index():
    aluno = Aluno.query.all()
    return render_template('index.html', alunos=aluno)


@app.route('/novo_professor', methods=['GET', 'POST'])
def novo_professor():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        verificar = Professor.query.filter_by(pro_email=email).first()

        if not verificar:
            novo_prof = Professor(pro_nome=nome, pro_email=email)
            db.session.add(novo_prof)
            db.session.commit()

            flash('Professor cadastrado com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Professor já cadastrado.', category='error')
        return redirect(url_for('novo_professor'))

    return render_template('professor.html')

@app.route('/nova_disciplina', methods=['GET', 'POST'])
def nova_disciplina():
    if request.method == 'POST':
        nome = request.form['nome']
        prof = request.form['prof']
        
        verificar = Disciplina.query.filter_by(dis_nome=nome).first()
    
        if not verificar:
            nova_dis = Disciplina(dis_nome=nome, dis_pro_id=prof) 
            db.session.add(nova_dis)
            db.session.commit()

            flash('Nova disciplina cadastrada com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Não foi possível adicionar a nova disciplina.', category='error')
        return redirect(url_for('nova_disciplina'))
    
    prof = Professor.query.all()
    if not prof:
        flash('Ainda não há professores cadastrados.', category='error')
        return redirect(url_for('index'))
    return render_template('disciplina.html', professores=prof)

@app.route('/novo_aluno', methods=['GET', 'POST'])
def novo_aluno():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        verificar = Aluno.query.filter_by(alu_email=email).first()

        if not verificar:
            novo_aluno = Aluno(alu_nome=nome, alu_email=email)
            db.session.add(novo_aluno)
            db.session.commit()

            flash('Aluno cadastrado com sucesso!', category='success')
            return redirect(url_for('index'))
        
        flash('Aluno já cadastrado.', category='error')
        return redirect(url_for('novo_aluno'))
    
    return render_template('aluno.html')

@app.route('/matricular', methods=['GET', 'POST'])
def matricular():
    if request.method == 'POST':
        aluno_id = request.form['aluno']
        disciplina_id = request.form['disciplina']

        aluno = Aluno.query.get(aluno_id)
        disciplina = Disciplina.query.get(disciplina_id)

        if disciplina not in aluno.disciplina:
            aluno.disciplina.append(disciplina)
            db.session.commit()

            flash('Aluno matriculado com sucesso!', category='success')
            return redirect(url_for('index'))

        flash('O aluno já possui a disciplina.', category='error')


    alunos = Aluno.query.all()
    disciplinas = Disciplina.query.all()
    if not alunos or not disciplinas:
        flash('Ainda não há alunos ou disciplinas cadastradas.', category='error')
        return redirect(url_for('index'))
    return render_template('matricular.html', alunos=alunos, disciplinas=disciplinas)
