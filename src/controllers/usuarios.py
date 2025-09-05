from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.usuarios_model import Usuarios
from src.validators.usuario_validator import validar_usuario
from config_db import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import or_
import re
import re
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
        # Limpa o telefone, removendo tudo que não for dígito
        telefone_limpo = re.sub(r'\D', '', telefone)
        # Passa o telefone limpo para o validador
        erros = validar_usuario(nome, email, senha, confirmar_senha, telefone_limpo)
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return redirect(url_for('usuarios.cadastro'))

        novo_usuario = Usuarios(
            nome = nome, 
            email = email, 
            senha = senha_hash, 
            telefone = telefone_limpo
        )
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('usuarios.login'))
    
    return render_template('cadastro.html')

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identificador = request.form['identificador']
        senha = request.form['senha']
        telefone_limpo = re.sub(r'\D', '', identificador)
        # Procura o usuário por email ou pelo telefone
        usuario = Usuarios.query.filter(
            or_(Usuarios.email == identificador, Usuarios.telefone == telefone_limpo)
        ).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            flash(f'Login realizado com sucesso! Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('home.index'))
        else:
            flash('Email/Telefone ou senha inválidos. Tente novamente.', 'error')
            return redirect(url_for('usuarios.login'))

    return render_template('login.html')

@usuarios_bp.route('/perfil')
def perfil():
    return render_template('perfil.html')

@usuarios_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('home.index'))