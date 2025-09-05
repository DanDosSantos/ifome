from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.usuarios_model import Usuarios
from src.validators.usuario_validator import validar_usuario
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import or_
from extensions import db, oauth
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

@usuarios_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('usuarios.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@usuarios_bp.route('/login/google/callback')
def authorize_google():
    token = oauth.google.authorize_access_token()
    user_info = token['userinfo']
    
    # Checa se o usuário já existe no banco de dados
    usuario = Usuarios.query.filter_by(email=user_info['email']).first()
    
    if not usuario:
        # Se o usuário não existe, cria uma nova conta
        # Nota: A senha pode ser gerada aleatoriamente ou deixada nula se a sua lógica permitir
        # Aqui, vamos gerar uma senha aleatória forte pois nosso modelo exige uma.
        senha_aleatoria = generate_password_hash(os.urandom(16).hex())

        novo_usuario = Usuarios(
            nome=user_info['name'],
            email=user_info['email'],
            senha=senha_aleatoria # Senha aleatória, pois o login será via Google
        )
        db.session.add(novo_usuario)
        db.session.commit()
        usuario = novo_usuario

    # Inicia a sessão para o usuário
    session['usuario_id'] = usuario.id
    session['usuario_nome'] = usuario.nome
    
    flash('Login com Google realizado com sucesso!', 'success')
    return redirect(url_for('home.index'))

@usuarios_bp.route('/login/facebook')
def login_facebook():
    redirect_uri = url_for('usuarios.authorize_facebook', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@usuarios_bp.route('/login/facebook/callback')
def authorize_facebook():
    token = oauth.facebook.authorize_access_token()
    
    # Busca as informações do usuário no Facebook
    resp = oauth.facebook.get('me?fields=id,name,email')
    user_info = resp.json()
    
    # O email é a nossa chave para encontrar ou criar o usuário
    user_email = user_info.get('email')
    user_name = user_info.get('name')

    if not user_email:
        flash('Não foi possível obter o e-mail do Facebook. Por favor, tente outro método de login.', 'error')
        return redirect(url_for('usuarios.login'))

    # Checa se o usuário já existe no nosso banco de dados
    usuario = Usuarios.query.filter_by(email=user_email).first()

    if not usuario:
        # Se não existe, cria um novo usuário
        senha_aleatoria = generate_password_hash(os.urandom(16).hex())
        novo_usuario = Usuarios(
            nome=user_name,
            email=user_email,
            senha=senha_aleatoria
        )
        db.session.add(novo_usuario)
        db.session.commit()
        usuario = novo_usuario
    
    # Inicia a sessão para o usuário
    session['usuario_id'] = usuario.id
    session['usuario_nome'] = usuario.nome

    flash('Login com Facebook realizado com sucesso!', 'success')
    return redirect(url_for('home.index'))