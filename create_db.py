# create_db.py
from config_db import db
import os

# IMPORTAR TODOS OS MODELOS AQUI
from src.models.usuarios_model import Usuarios, Endereco, Restaurante, Produto
# Importe quaisquer outros modelos que você tenha

# --- NOVO: Limpa a MetaData existente ---
# Isso garante que não há tabelas pré-definidas de execuções anteriores ou imports ocultos.
db.metadata.clear()
# -------------------------------------

from flask import Flask
app = Flask(__name__)

# Configurações do banco de dados TEMPORÁRIAS para este script
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/ifome.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    instance_path = os.path.join(app.root_path, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    db_full_path = os.path.join(instance_path, 'ifome.db')

    if os.path.exists(db_full_path):
        try:
            os.remove(db_full_path)
            print(f"Arquivo DB existente '{db_full_path}' removido com sucesso.")
        except Exception as e:
            print(f"AVISO: Não foi possível remover o arquivo DB '{db_full_path}'. Pode estar em uso. Erro: {e}")
            print("Por favor, garanta que nenhum processo está a aceder ao banco de dados e tente novamente.")
            exit()

    db.create_all()
    print("Banco de dados 'ifome.db' e tabelas criadas com sucesso!")