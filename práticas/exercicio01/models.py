from sqlalchemy import create_engine, String, Float, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from flask_login import UserMixin
from typing import List

engine = create_engine('sqlite:///usutimes.db')
session = Session(bind=engine)

class Base(UserMixin, DeclarativeBase):
    pass

users_times = Table('users_times',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('time_id', ForeignKey('times.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(150))
    email:Mapped[str] = mapped_column(String(150), unique=True)
    senha:Mapped[str] = mapped_column(String)

    times:Mapped[List['Time']] = relationship(secondary=users_times, back_populates='users')

class Time(Base):
    __tablename__ = 'times'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(150), unique=True)

    users:Mapped[List['User']] = relationship(secondary=users_times, back_populates='times')

Base.metadata.create_all(bind=engine)