from flask import Blueprint, render_template

restaurantes_bp = Blueprint('restaurantes', __name__, template_folder='../templates')

@restaurantes_bp.route('/restaurantes/cadastro')
def cadastro_restaurante():
    return render_template('cadastro_restaurante.html')