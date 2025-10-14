from config_db import db

class Restaurante(db.Model):
    __tablename__ = 'restaurante'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    categoria = db.Column(db.String(50))
    email_responsavel = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    nome_responsavel = db.Column(db.String(100))
    cpf_responsavel = db.Column(db.String(20))
    telefone_responsavel = db.Column(db.String(15))
    hora_abertura = db.Column(db.Time, nullable=False)
    hora_fechamento = db.Column(db.Time, nullable=False)
    imagem_restaurante = db.Column(db.String(255))
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=True)

    endereco = db.relationship('Endereco', backref='restaurante', uselist=False)

    def __init__(self, nome, cnpj, telefone, categoria, senha, nome_responsavel, cpf_responsavel, email_responsavel, telefone_responsavel, hora_abertura, hora_fechamento, endereco=None, imagem_restaurante=None):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.categoria = categoria
        self.senha = senha
        self.endereco = endereco
        self.nome_responsavel = nome_responsavel
        self.cpf_responsavel = cpf_responsavel
        self.email_responsavel = email_responsavel
        self.telefone_responsavel = telefone_responsavel
        self.hora_abertura = hora_abertura
        self.hora_fechamento = hora_fechamento
        self.imagem_restaurante = imagem_restaurante

    def __repr__(self):
        return f'<Restaurante {self.nome}>'
    
from src.models.endereco_model import Endereco
Restaurante.endereco = db.relationship("Endereco", backref="restaurante", uselist=False)