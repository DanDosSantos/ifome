from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.usuarios_model import Usuarios
from src.validators.usuario_validator import validar_usuario
from config_db import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import os

usuarios_bp = Blueprint('usuarios', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@usuarios_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        confirmar_senha = request.form['confirmar_senha']
        telefone = request.form['telefone']

        erros = validar_usuario(nome, email, senha, confirmar_senha, telefone)
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return redirect(url_for('usuarios.cadastro'))

        novo_usuario = Usuarios(
            nome = nome, 
            email = email, 
            senha = senha_hash, 
            telefone = telefone
        )
        db.session.add(novo_usuario)
        db.session.commit()
        
        return redirect(url_for('usuarios.login'))
    
    return render_template('cadastro.html')

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuarios.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            flash(f'Login realizado com sucesso! Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('home.index'))
        else:
            flash('Email ou senha inválidos. Tente novamente.', 'error')
            return redirect(url_for('usuarios.login'))

    return render_template('login.html')