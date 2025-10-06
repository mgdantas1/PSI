from sqlalchemy import create_engine, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from flask_login import UserMixin

engine = create_engine('mysql://root:@localhost/tarefas')
session = Session(bind=engine)

class Base(UserMixin, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha:Mapped[str] = mapped_column(String(200), nullable=False)

    tarefas = relationship('Tarefa', backref='users')

class Tarefa(Base):
    __tablename__ = 'tarefas'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tarefa:Mapped[str] = mapped_column(String(150), nullable=False)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))


Base.metadata.create_all(bind=engine)
