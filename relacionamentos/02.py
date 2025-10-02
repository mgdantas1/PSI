from base import *

#   RELACIONAMENTO N:N

alunos_cursos = Table('alunos_cursos',
    Base.metadata,
    Column('aluno_id', ForeignKey('alunos.id'), primary_key=True),
    Column('curso_id', ForeignKey('cursos.id'), primary_key=True)
)

class Aluno(Base):
    __tablename__ = 'alunos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(150))

    # o nome em back_populates deve ser o mesmo nome que está no atributo da outra tabela, nesse caso será "alunos", pois foi nomeado assim na outra tabela
    cursos:Mapped[List['Curso']] = relationship(secondary=alunos_cursos, back_populates='alunos')


class Curso(Base):
    __tablename__ = 'cursos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(150))

    alunos:Mapped[List['Aluno']] = relationship(secondary=alunos_cursos, back_populates='cursos')

Base.metadata.create_all(bind=engine)

session.begin()

curso1 = Curso(nome='Informática')
curso2 = Curso(nome='Eletrotécnica')

session.add_all([curso1, curso2])

alu1 = Aluno(nome='Maria')
alu2 = Aluno(nome='João')

session.add_all([alu1, alu2])

# preenchendo a tabela associativa
alu1.cursos.append(curso1)
alu2.cursos.append(curso2)

# também poderia fazer...
# curso1.alunos.append(alu1)
# curso2.alunos.append(alu2)

# descobrindo o curso do alu1
aluno = session.query(Aluno).where(Aluno.id == 1).first()
curso = aluno.cursos
for i in curso:
    print(i.nome)

session.commit()
session.close()