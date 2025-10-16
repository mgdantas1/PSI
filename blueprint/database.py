from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Session, DeclarativeBase, relationship
from flask_login import UserMixin

engine = create_engine('sqlite:///banco.db')


class Base(UserMixin, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(200))
    email:Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha:Mapped[str] = mapped_column(String(200), nullable=False)

    livros = relationship('Livro', backref='users')

class Livro(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo:Mapped[str] = mapped_column(String(100))
    genero:Mapped[str] = mapped_column(String(100))
    autor:Mapped[str] = mapped_column(String(100))
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

Base.metadata.create_all(bind=engine)