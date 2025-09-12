# src/controllers/produtos.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from config_db import db
from src.models.usuarios_model import Produto 

produtos_bp = Blueprint('produtos', __name__, template_folder='../templates', static_folder='../static')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@produtos_bp.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('listar_produtos.html', produtos=produtos)

@produtos_bp.route('/produtos/cadastro', methods=['GET'])
def form_cadastro_produto():
    return render_template('cadastro_produto.html')

@produtos_bp.route('/produtos/cadastro', methods=['POST'])
def cadastrar_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    categoria = request.form['categoria']

    imagem = request.files.get('imagem')
    nome_imagem = ''
    if imagem and imagem.filename:
        nome_imagem = secure_filename(imagem.filename)
        imagem.save(os.path.join(UPLOAD_FOLDER, nome_imagem))

    novo_produto = Produto(
        nome=nome,
        descricao=descricao,
        preco=float(preco),
        categoria=categoria,
        imagem=nome_imagem
    )

    db.session.add(novo_produto)
    db.session.commit()

    flash('Produto cadastrado com sucesso!', 'success')
    return redirect(url_for('produtos.listar_produtos'))