import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.base import Base
from model.processo import Processo

db_path = "database/"
if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = f'sqlite:///{db_path}db.sqlite3'

engine = create_engine(db_url, echo=False, connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)

# Cria as tabelas no banco
Base.metadata.create_all(engine)
