from models import Base
from models.users import User
from models.products import Products
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database/base.db')
Base.metadata.create_all(bind=engine)