from config_db import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=True)

    # relação para acessar o endereço direto
    endereco = db.relationship('Endereco', backref='usuario', uselist=False) 

    def __init__(self, nome, email, senha, telefone, endereco=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.endereco = endereco

    def __repr__(self):
        return f'<Usuario {self.nome}>'


class Endereco(db.Model):
    __tablename__ = 'endereco'
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(150))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(20))

class Restaurante(db.Model):
    __tablename__ = 'restaurante'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=False)
    
    endereco = db.relationship('Endereco', backref='restaurante', uselist=False)
    produtos = db.relationship('Produto', backref='restaurante', lazy=True)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50))
    imagem = db.Column(db.String(100), nullable=True)
    
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    
# class Restaurante(db.Model):
#     __tablename__ = 'restaurante'

#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100))
#     cnpj = db.Column(db.String(20))
#     telefone = db.Column(db.String(15))
#     endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'))
#     categoria = db.Column(db.String(50))

#     endereco = db.relationship('Endereco')

#     def __repr__(self):
#         return f'<Restaurante {self.nome}>'
    

# class Cardapio(db.Model):
#     __tablename__ = 'cardapio'

#     id = db.Column(db.Integer, primary_key=True)
#     restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'))
#     nome_cardapio = db.Column(db.String(100))

#     restaurante = db.relationship('Restaurante')

#     def __repr__(self):
#         return f'<Cardapio {self.nome_cardapio}>'


# class ItemCardapio(db.Model):
#     __tablename__ = 'item_cardapio'

#     id = db.Column(db.Integer, primary_key=True)
#     cardapio_id = db.Column(db.Integer, db.ForeignKey('cardapio.id'))
#     restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'))
#     nome_item = db.Column(db.String(100))
#     descricao = db.Column(db.String(200))
#     preco = db.Column(db.Float)
#     disponivel = db.Column(db.Boolean, default=True)

#     cardapio = db.relationship('Cardapio')
#     restaurante = db.relationship('Restaurante')

#     def __repr__(self):
#         return f'<ItemCardapio {self.nome_item}>'
    
# class Pedido(db.Model):
#     __tablename__ = 'pedido'

#     id = db.Column(db.Integer, primary_key=True)
#     usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
#     restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'))
#     data_hora = db.Column(db.DateTime)
#     status = db.Column(db.String(20))  # em_preparo, a_caminho, entregue
#     valor_total = db.Column(db.Float)

#     usuario = db.relationship('Usuarios')
#     restaurante = db.relationship('Restaurante')
#     itens = db.relationship('ItemPedido', backref='pedido', cascade="all, delete-orphan")
#     pagamento = db.relationship('Pagamento', uselist=False, backref='pedido')
#     entrega = db.relationship('Entrega', uselist=False, backref='pedido')

#     def __repr__(self):
#         return f'<Pedido {self.id}>'
    
# class ItemPedido(db.Model):
#     __tablename__ = 'item_pedido'

#     id = db.Column(db.Integer, primary_key=True)
#     pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
#     item_cardapio_id = db.Column(db.Integer, db.ForeignKey('item_cardapio.id'))
#     quantidade = db.Column(db.Integer)
#     preco_unitario = db.Column(db.Float)

#     item_cardapio = db.relationship('ItemCardapio')

#     def __repr__(self):
#         return f'<ItemPedido {self.id}>'
    
# class Pagamento(db.Model):
#     __tablename__ = 'pagamento'

#     id = db.Column(db.Integer, primary_key=True)
#     pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
#     forma_pagamento = db.Column(db.String(20))  # cartao, pix, dinheiro
#     status_pagamento = db.Column(db.String(20))  # pendente, aprovado, recusado
#     valor_pago = db.Column(db.Float)

#     def __repr__(self):
#         return f'<Pagamento {self.id}>'
    

# class Entregador(db.Model):
#     __tablename__ = 'entregador'

#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100))
#     cpf = db.Column(db.String(20))
#     telefone = db.Column(db.String(15))
#     veiculo = db.Column(db.String(10))  # moto, bike, carro

#     def __repr__(self):
#         return f'<Entregador {self.nome}>'
    

# class Entrega(db.Model):
#     __tablename__ = 'entrega'

#     id = db.Column(db.Integer, primary_key=True)
#     pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
#     entregador_id = db.Column(db.Integer, db.ForeignKey('entregador.id'))
#     previsao_entrega = db.Column(db.DateTime)
#     data_entrega = db.Column(db.DateTime)
#     status_entrega = db.Column(db.String(20))  # pendente, em_rota, finalizada

#     entregador = db.relationship('Entregador')

#     def __repr__(self):
#         return f'<Entrega {self.id}>'