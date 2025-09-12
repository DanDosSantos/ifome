from flask import Flask
import os
from dotenv import load_dotenv
from config_db import db
from src.controllers.produtos import produtos_bp
def create_app():
    app = Flask(__name__)
    
    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ifome.db'  # Exemplo com SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Inicializa o SQLAlchemy com o app
    db.init_app(app)

    from src.controllers.usuarios import usuarios_bp
    from src.controllers.home import home_bp
    from src.controllers.restaurantes import restaurantes_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)
<<<<<<< HEAD
    app.register_blueprint(produtos_bp)
=======
    app.register_blueprint(restaurantes_bp)
>>>>>>> d5340049f1e95937d6915cecb6b784764a71f320

    return app

# Este bloco só será executado quando você rodar o script diretamente
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
    