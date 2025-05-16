from datetime import datetime
from db import db

class Processo(db.Model):
    __tablename__ = 'processo'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)

    numero = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    data_insercao = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, usuario_id, numero, descricao, data_inicio, data_fim, data_insercao=None):
        self.usuario_id = usuario_id
        self.numero = numero
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.data_insercao = data_insercao or datetime.now()
