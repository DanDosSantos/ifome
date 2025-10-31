from config_db import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=True)

    # relação para acessar o endereço direto
    endereco = db.relationship('Endereco', backref='usuario', uselist=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'
        
from src.models.endereco_model import Endereco
Usuarios.endereco = db.relationship("Endereco", backref="usuario", uselist=False)
