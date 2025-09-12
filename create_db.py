from app import create_app
from config_db import db
import os

app = create_app()

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