from models import Base, create_engine

from flask import Flask

engine = create_engine('sqlite:///database/bade.db')

Base.metadata.create_all(bind=engine)

app = Flask(__name__)


