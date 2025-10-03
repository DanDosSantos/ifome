from flask import Blueprint, render_template, request, jsonify
from config_db import db
from src.models.restaurante_model import Restaurante
from src.models.endereco_model import Endereco
from datetime import datetime
from werkzeug.security import generate_password_hash

restaurante_bp = Blueprint('restaurante', __name__, template_folder='../templates')

@restaurante_bp.route('/restaurante', methods=['GET'])
def cadastro():
    return render_template('restaurante.html')

@restaurante_bp.route('/restaurante/login', methods=['GET', 'POST'])
def login():
    return render_template('login-parceiro.html')

# CREATE
@restaurante_bp.route('/api/restaurantes', methods=['POST'])
def create_restaurante():
    data = request.json

    # Cria endereço primeiro
    endereco = Endereco(
        cep=data["cep"],
        rua=data["rua"],
        numero=data["numero"],
        bairro=data["bairro"],
        cidade=data["cidade"],
        estado=data["estado"],
    )
    db.session.add(endereco)
    db.session.flush()  # pega o id do endereço

    hora_abertura = datetime.strptime(data['horario_abertura'], "%H:%M").time()
    hora_fechamento = datetime.strptime(data['horario_fechamento'], "%H:%M").time()
    senha_hash = generate_password_hash(data["senha"])

    # Cria restaurante
    restaurante = Restaurante(
        nome=data["nome_estabelecimento"],
        cnpj=data["cnpj"],
        telefone=data["telefone"],
        categoria=data["categoria"],
        senha=senha_hash,
        nome_responsavel=data["nome_responsavel"],
        cpf_responsavel=data["cpf_responsavel"],
        email_responsavel=data["email_responsavel"],
        telefone_responsavel=data["telefone_responsavel"],
        hora_abertura=hora_abertura,
        hora_fechamento=hora_fechamento,
        endereco=endereco
    )

    db.session.add(restaurante)
    db.session.commit()

    return jsonify({"message": "Restaurante criado!", "id": restaurante.id}), 201

# READ - lista todos
# Bater nessa rota de todos os restaurantes, vai fazer uma query no banco de dados para buscar todos os restaurantes
# Bem provável que seja a rota para bater ao pesquisar por restaurantes 
@restaurante_bp.route("/api/restaurantes", methods=["GET"])
def get_restaurantes():
    restaurantes = Restaurante.query.all()
    return jsonify([
        {
            "id": r.id,
            "nome": r.nome,
            "categoria": r.categoria,
            "telefone": r.telefone,
            "responsavel": r.nome_responsavel,
            "hora_abertura": str(r.hora_abertura),
            "hora_fechamento": str(r.hora_fechamento),
            "endereco": {
                "rua": r.endereco.rua if r.endereco else None,
                "numero": r.endereco.numero if r.endereco else None,
                "cidade": r.endereco.cidade if r.endereco else None
            }
        }
        for r in restaurantes
    ])

# Exemplo de rota de busca
@restaurante_bp.route('/api/restaurantes/busca')
def buscar_restaurantes():
    termo = request.args.get('q', '')
    restaurantes = Restaurante.query.filter(
        Restaurante.nome.ilike(f"%{termo}%")
    ).all()
    return jsonify([{
        "id": r.id,
        "nome": r.nome,
        "categoria": r.categoria,
        # ...outros campos que quiser retornar
    } for r in restaurantes])

# READ - detalhe
# Bater nessa rota, vai fazer uma query no banco de dados para buscar um restaurante específico de acordo com seu id
@restaurante_bp.route("/api/restaurantes/<int:id>", methods=["GET"])
def get_restaurante(id):
    r = Restaurante.query.get_or_404(id)
    return jsonify({
        "id": r.id,
        "nome": r.nome,
        "categoria": r.categoria,
        "telefone": r.telefone,
        "responsavel": r.nome_responsavel,
        "hora_abertura": str(r.hora_abertura),
        "hora_fechamento": str(r.hora_fechamento),
        "endereco": {
            "rua": r.endereco.rua if r.endereco else None,
            "numero": r.endereco.numero if r.endereco else None,
            "cidade": r.endereco.cidade if r.endereco else None
        }
    })


# UPDATE
@restaurante_bp.route("/api/restaurantes/<int:id>", methods=["PUT"])
def update_restaurante(id):
    data = request.json
    restaurante = Restaurante.query.get_or_404(id)

    for key, value in data.items():
        if hasattr(restaurante, key):
            setattr(restaurante, key, value)

    db.session.commit()
    return jsonify({"message": "Restaurante atualizado!"})


# DELETE
@restaurante_bp.route("/api/restaurantes/<int:id>", methods=["DELETE"])
def delete_restaurante(id):
    restaurante = Restaurante.query.get_or_404(id)
    db.session.delete(restaurante)
    db.session.commit()
    return jsonify({"message": "Restaurante excluído!"})