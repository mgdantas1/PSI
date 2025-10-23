from models import Base
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Products(Base):
    __tablename__ = 'produtos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(150), unique=True)
    preco:Mapped[float] = mapped_column(Float)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

