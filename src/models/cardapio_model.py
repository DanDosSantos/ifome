from config_db import db
from sqlalchemy import Time

class Cardapio(db.Model):
    __tablename__ = 'cardapios'

    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    nome_cardapio = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    restaurante = db.relationship('Restaurante', backref='cardapios', lazy=True)

    produtos = db.relationship(
        "Produto",
        back_populates="cardapio",
        lazy=True,
        cascade="all, delete-orphan"  # faz a exclusão automática dos produtos
    )

    def __init__(self, nome_cardapio, restaurante_id, ativo=True):
        self.nome_cardapio = nome_cardapio
        self.restaurante_id = restaurante_id
        self.ativo = ativo

    def __repr__(self):
        return f"<Cardapio {self.nome_cardapio}>"
    
