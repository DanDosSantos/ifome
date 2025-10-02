from flask import Blueprint, render_template

restaurante_bp = Blueprint('restaurante', __name__, template_folder='../templates')

@restaurante_bp.route('/restaurante')
def cadastro():
    return render_template('restaurante.html')