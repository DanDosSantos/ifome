from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, template_folder='../templates')

@home_bp.route('/')
def index():
    return render_template('index.html')

@home_bp.route('/parceiros')
def parceiros():
    return render_template('parceiros.html')