from flask import Blueprint, render_template, request, redirect, url_for
from src.models.usuarios_model import Usuarios
from config_db import db
from werkzeug.security import generate_password_hash
import os

usuarios_bp = Blueprint('usuarios', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@usuarios_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        telefone = request.form['telefone']

        novo_usuario = Usuarios(
            nome = nome, 
            email = email, 
            senha = senha_hash, 
            telefone = telefone
        )
        db.session.add(novo_usuario)
        db.session.commit()
        
        return "cadastro realizado com sucesso!"
    
    return render_template('cadastro.html')