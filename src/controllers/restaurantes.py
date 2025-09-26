# src/controllers/restaurantes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config_db import db
from src.models.usuarios_model import Restaurante, Endereco
from werkzeug.security import generate_password_hash, check_password_hash

restaurantes_bp = Blueprint('restaurantes', __name__, url_prefix='/parceiros', template_folder='../templates')

@restaurantes_bp.route('/cadastro', methods=['GET'])
def form_cadastro():
    return render_template('cadastro_restaurante.html')

@restaurantes_bp.route('/cadastro', methods=['POST'])
def cadastrar():
    flash('Restaurante cadastrado com sucesso! Aguarde a aprovação.', 'success')
    return redirect(url_for('restaurantes.form_cadastro'))

# Rota para login de parceiros
@restaurantes_bp.route('/login', methods=['GET', 'POST'])
def login():
    return "Página de Login de Parceiros"

# Painel principal do parceiro (requer login)
@restaurantes_bp.route('/painel')
def painel():
    if 'restaurante_id' not in session:
        return redirect(url_for('restaurantes.login'))
    
    restaurante = Restaurante.query.get(session['restaurante_id'])
    return render_template('painel_restaurante.html', restaurante=restaurante)

@restaurantes_bp.route('/produtos')
def listar_produtos():
    if 'restaurante_id' not in session:
        return redirect(url_for('restaurantes.login'))
    
    produtos = Produto.query.filter_by(restaurante_id=session['restaurante_id']).all()
    return render_template('listar_produtos.html', produtos=produtos)

# As rotas de cadastrar, editar e excluir produtos também serão adicionadas aqui.