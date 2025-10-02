from config_db import db
from sqlalchemy import Time

class Restaurante(db.Model):
    __tablename__ = 'restaurante'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(15))
    categoria = db.Column(db.String(50))
    nome_responsavel = db.Column(db.String(100))
    cpf_responsavel = db.Column(db.String(20))
    email_responsavel = db.Column(db.String(100))
    telefone_responsavel = db.Column(db.String(15))
    hora_abertura = db.Column(db.Time, nullable=False)
    hora_fechamento = db.Column(db.Time, nullable=False)
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=True)

    endereco = db.relationship('Endereco', backref='restaurante', uselist=False)

    def __init__(self, nome, cnpj, telefone, categoria, nome_responsavel, cpf_responsavel, email_responsavel, telefone_responsavel, hora_abertura, hora_fechamento, endereco=None):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.categoria = categoria
        self.endereco = endereco
        self.nome_responsavel = nome_responsavel
        self.cpf_responsavel = cpf_responsavel
        self.email_responsavel = email_responsavel
        self.telefone_responsavel = telefone_responsavel
        self.hora_abertura = hora_abertura
        self.hora_fechamento = hora_fechamento

    def __repr__(self):
        return f'<Restaurante {self.nome}>'
    
from src.models.endereco_model import Endereco
Restaurante.endereco = db.relationship("Endereco", backref="restaurante", uselist=False)