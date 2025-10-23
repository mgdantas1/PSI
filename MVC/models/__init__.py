from sqlalchemy import create_engine, String, Float, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from flask_login import UserMixin

class Base(UserMixin, DeclarativeBase):
    pass