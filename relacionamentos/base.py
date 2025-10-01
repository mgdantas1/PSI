from sqlalchemy import String, Float, ForeignKey, create_engine, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from typing import List

engine = create_engine('mysql://root:@localhost/pratica')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass