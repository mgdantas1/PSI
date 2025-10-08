from sqlalchemy import create_engine, String, Float, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from flask_login import UserMixin
from typing import List

engine = create_engine('mysql://root:@localhost/tarefas')

class Base(UserMixin, DeclarativeBase):
    pass

# tabela associativa N:N
tarefas_categoria = Table('tarefas_categoria',
    Base.metadata,
    Column('categoria_id', ForeignKey('categorias.id'), primary_key=True),
    Column('tarefa_id', ForeignKey('tarefas.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha:Mapped[str] = mapped_column(String(200), nullable=False)

    tarefas:Mapped[List['Tarefa']] = relationship('Tarefa', backref='users')

class Tarefa(Base):
    __tablename__ = 'tarefas'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tarefa:Mapped[str] = mapped_column(String(150), nullable=False)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

    # N:N
    categoria:Mapped[List['Categoria']] = relationship(secondary='tarefas_categoria', back_populates='tarefas')

class Categoria(Base):
    __tablename__ = 'categorias'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    categoria:Mapped[str] = mapped_column(String(150))

    # N:N
    tarefas:Mapped[List['Tarefa']] = relationship(secondary='tarefas_categoria', back_populates='categoria')

Base.metadata.create_all(bind=engine)


categorias = ["Trabalho", "Estudos", "Casa", "Lazer", "Saúde"]

with Session(bind=engine) as session:
    if session.query(Categoria).count() == 0:
        for cat in categorias:
            categoria = Categoria(categoria=cat)
            session.add(categoria)
        session.commit()


