from base import *

#   RELACIONAMENTO 1:N

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(150))

    # serve como atalho
    post = relationship('Post', backref='user')

class Post(Base):
    __tablename__ = 'posts'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    texto:Mapped[str] = mapped_column(String(500))

    # chave estrangeira
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

Base.metadata.create_all(bind=engine)

user1 = User(nome='Maria', email='maria@gmail')
user2 = User(nome='João', email='joao@gmail')
post1 = Post(texto='Olá, mundo!', user_id=1)
post2 = Post(texto='Hello, mundo!', user_id=1)
post3 = Post(texto='Oi!', user_id=2)


session.begin()

session.add_all([user1, user2])
# ou...
# session.add(user1)
# session.add(user2)
session.add_all([post1, post2, post3])

session.commit()
session.close()

# -- teste para descobrir os posts do user1
# fazer consulta...
user = session.query(User).where(User.id == 1).first()
# ou...
# user = session.query(User).filter_by(id = 1).first()

# -- aqui estou utilizando aquele "atalho" para conseguir descobrir todos os posts do usuário de forma mais rápida
posts = user.post
for i in posts:
    print(i.texto)

