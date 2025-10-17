from flask import Blueprint, render_template, request, redirect, jsonify, url_for, flash, session
from config_db import db
from src.validators.restaurante_validator import validar_restaurante
from src.models.restaurante_model import Restaurante
from src.models.endereco_model import Endereco
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import re, os

restaurante_bp = Blueprint('restaurante', __name__, template_folder='../templates')

UPLOAD_FOLDER = 'src/static/uploads'

# Template de cadastro de restaurante
@restaurante_bp.route('/restaurante', methods=['GET'])
def cadastro():
    return render_template('restaurante.html')

# Template de login de restaurante
@restaurante_bp.route('/restaurante/login', methods=['GET'])
def login():
    return render_template('login-parceiro.html')

# TODO: Corrigir o redirecionamento de logout para a aba de parceiros
@restaurante_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect('/parceiros')

@restaurante_bp.route('/portal-parceiro')
def portal_parceiro():
    restaurante = Restaurante.query.get(session.get('restaurante_id'))
    return render_template('portal-parceiro.html', restaurante=restaurante)

# Quando clica em Entrar no login de parceiro ele bate nessa rota da API que busca as informações do banco em json para verificar se esta correto e fazer o login
@restaurante_bp.route('/api/restaurante/login', methods=['POST'])
def api_login_restaurante():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    restaurante = Restaurante.query.filter_by(email_responsavel=email).first()
    if restaurante and check_password_hash(restaurante.senha, senha):
        session['restaurante_id'] = restaurante.id  # Adiciona o ID do restaurante na sessão
        return jsonify({"message": "Login realizado com sucesso!", "id": restaurante.id}), 200
    else:
        return jsonify({"message": "Email ou senha inválidos"}), 401

# CREATE, quando eu crio o form de restaurante bate nessa API que cadastra no banco de dados as informações do restaurante
@restaurante_bp.route('/api/restaurantes', methods=['POST'])
def create_restaurante():
    data = request.form
    imagem = request.files.get('imagem_restaurante')

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

    # Chama o validator
    erros = validar_restaurante(
        nome=data.get("nome_estabelecimento"),
        cnpj=data.get("cnpj"),
        email=data.get("email_responsavel"),
        telefone=data.get("telefone"),
        senha=data.get("senha"),
        confirmar_senha=data.get("confirmar_senha"),
        cpf=data.get("cpf_responsavel"),
        tel_resp=data.get("telefone_responsavel"),
        hora_abertura=data.get("horario_abertura"),
        hora_fechamento=data.get("horario_fechamento")
    )
    if erros:
        return jsonify({"errors": erros}), 400
    
    imagem_path = None
    if imagem and imagem.filename:
        filename = secure_filename(imagem.filename)
        imagem_path = os.path.join(UPLOAD_FOLDER, filename)
        imagem.save(imagem_path)  

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
        endereco=endereco,
        imagem_restaurante=imagem_path
    )

    db.session.add(restaurante)
    db.session.commit()

    return jsonify({"message": "Restaurante criado! Faça login no portal do parceiro para continuar.", "id": restaurante.id}), 201

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
        "imagem_restaurante": r.imagem_restaurante,
        # ...outros campos que quiser retornar
    } for r in restaurantes])

# READ - rota da API que retorna JSON
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

# READ - rota da página HTML
@restaurante_bp.route('/restaurante/<int:id>', methods=['GET'])
def get_restaurante_page(id):
    return render_template('info_restaurante.html', restaurante_id=id)


# UPDATE
@restaurante_bp.route("/api/restaurantes/<int:id>", methods=["PUT"])
def update_restaurante(id):
    data = request.json
    restaurante = Restaurante.query.get_or_404(id)

    for key, value in data.items():
        if key in ['hora_abertura', 'hora_fechamento'] and isinstance(value, str):
            value = datetime.strptime(value, "%H:%M").time()
        if hasattr(restaurante, key):  # Se o restaurante tem esse atributo.. restaurante e key
            setattr(restaurante, key, value) # atualiza o valor com setattr(restaurante, key, value)

    db.session.commit()
    return jsonify({"message": "Restaurante atualizado!"})


# DELETE
@restaurante_bp.route("/api/restaurantes/<int:id>", methods=["DELETE"])
def delete_restaurante(id):
    restaurante = Restaurante.query.get_or_404(id)
    db.session.delete(restaurante)
    db.session.commit()
    return jsonify({"message": "Restaurante excluído!"})