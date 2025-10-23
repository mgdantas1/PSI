from models import Base, Mapped, mapped_column, String, relationship

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(150), unique=True)
    senha:Mapped[str] = mapped_column(String)

    produtos = relationship('Products', backref='users')

