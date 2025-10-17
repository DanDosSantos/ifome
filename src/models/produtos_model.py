from config_db import db

class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey("restaurante.id"), nullable=False)
    cardapio_id = db.Column(db.Integer, db.ForeignKey("cardapios.id"), nullable=False)  # ⚡ tabela correta
    nome_item = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True, nullable=False)

    cardapio = db.relationship("Cardapio", backref="itens_cardapio", lazy=True)
