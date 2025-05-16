from sqlalchemy import Column, Integer, String
from model.base import Base  # seu declarative base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(80), unique=True, nullable=False)
    senha = Column(String(256), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'
