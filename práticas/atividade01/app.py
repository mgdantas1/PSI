from flask import Flask, redirect, render_template, request, url_for, flash

from sqlalchemy import create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# conectando e integrando o banco de dados
engine = create_engine('sqlite:///database/banco.db')
# session para conseguir manipular o banco
Session = sessionmaker(bind=engine)
# é o modelo das tabelas
Base = declarative_base()


# criando a tabela (classe) de cursos

class Curso(Base):
    __tablename__ = 'curso'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    curso = Column(String(100), nullable=False, unique=True)

    aluno = relationship('Aluno', back_populates='curso')

# criando a tabela de aluno

class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    # chave estrangeira
    curso_id = Column(Integer, ForeignKey('curso.id'), nullable=False)

    curso = relationship('Curso', back_populates='aluno')


# criando as tabelas
Base.metadata.create_all(engine)

app = Flask(__name__)

app.secret_key = 'SECRETO'

@app.route('/')
def index():
    alunos = {}
    session = Session()
    tb_aluno = session.query(Aluno).all()
    for dados in tb_aluno:
        novo_aluno = {}
        novo_aluno['nome'] = dados.nome
        novo_aluno['email'] = dados.email
        curso = session.get(Curso, dados.curso_id)
        curso = curso.curso
        novo_aluno['curso'] = curso
        alunos[dados.id] = novo_aluno
    print(alunos)
    return render_template('index.html', alunos=alunos)

@app.route('/novo_curso', methods=['GET', 'POST'])
def novo_curso():
    if request.method == 'POST':
        curso = (request.form['curso']).strip().upper()
        session = Session()
        verificar_curso = session.query(Curso).filter_by(curso=curso).first()
        if not verificar_curso:
            novo_curso = Curso(curso=curso)
            session.add(novo_curso)
            session.commit()
            flash('Curso cadastrado com sucesso', category='success')
            return redirect(url_for('index'))
        session.close()
        flash('Curso já cadastrado', category='error')
        return redirect(url_for('novo_curso'))
    return render_template('curso.html')

@app.route('/novo_aluno', methods=['GET', 'POST'])
def novo_aluno():
    session = Session()
    cursos = session.query(Curso).all()
    if cursos:
        if request.method == 'POST':
            nome = request.form['nome']
            email = (request.form['email']).strip().lower()
            curso = request.form['cursos']

            verificar_email = session.query(Aluno).filter_by(email=email).first()

            if not verificar_email:
                cursos = session.query(Curso).filter_by(curso=curso).first()
                novo_aluno = Aluno(nome=nome, email=email, curso_id=cursos.id)
                session.add(novo_aluno)
                session.commit()
                session.close()
                flash('Aluno cadastrado com sucesso', category='success')
                return redirect(url_for('index'))
            
            session.close()
            flash('Aluno já cadastrado', category='error')
            return redirect(url_for('novo_aluno'))

        return render_template('aluno.html', cursos=cursos)
    
    flash('Ainda não há cursos cadastrados', category='error')
    return redirect(url_for('index'))

@app.route('/editar', methods=['GET', 'POST'])
def editar():
    session = Session()
    cursos = session.query(Curso).all()
    if cursos:
        if request.method == 'POST':
            email = request.form['email'].strip().lower()
            curso_novo = request.form['cursos']
            
            aluno = session.query(Aluno).filter_by(email=email).first()
            curso_antigo = session.query(Curso).filter_by(curso=curso_novo).first()

            if aluno:
                aluno.curso_id = curso_antigo.id
                session.commit()
                session.close()

                flash('Curso atualizado com sucesso', category='success')
                return redirect(url_for('index'))
        
            session.close()
            flash('O email pode estar incorreto', category='error')
            return redirect(url_for('editar'))

        return render_template('editar.html', cursos=cursos)
    
    flash('Ainda não há cursos cadastrados', category='error')
    return redirect(url_for('index'))

@app.route('/remover', methods=['GET', 'POST'])
def remover():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()

        session = Session()

        aluno = session.query(Aluno).filter_by(email=email).first()

        if aluno:
            session.delete(aluno)
            session.commit()
            session.close()

            flash('Aluno removido com sucesso', category='success')
            return redirect(url_for('index'))
        
        session.close()
        flash('O email pode estar incorreto', category='error')
        return redirect(url_for('editar'))
    
    return render_template('editar.html')

    