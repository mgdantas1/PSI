from models import Base, Mapped, mapped_column, String, relationship, Float, ForeignKey


class Products(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(150), unique=True)
    preco:Mapped[float] = mapped_column(Float)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

