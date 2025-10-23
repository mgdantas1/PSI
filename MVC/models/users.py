from models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

class User(UserMixin, Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(150), unique=True)
    senha:Mapped[str] = mapped_column(String)

    def get_id(self):
        return str(self.id)

    produtos = relationship('Products', backref='users')

