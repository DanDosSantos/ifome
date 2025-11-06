from flask import Flask
from flask_mail import Mail
from config_db import db
import os
from dotenv import load_dotenv

mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='src/static')
    
    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ifome.db'  # Exemplo com SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Config SMTP do Gmail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = ('iFome', os.getenv('MAIL_USERNAME'))
    
    # Inicializa o SQLAlchemy com o app
    db.init_app(app)
    mail.init_app(app)

    from src.controllers.usuarios import usuarios_bp
    from src.controllers.home import home_bp
    from src.controllers.restaurante import restaurante_bp
    from src.controllers.cardapio_controller import cardapio_bp
    from src.controllers.produto_controller import produto_bp


    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(restaurante_bp)
    app.register_blueprint(cardapio_bp)
    app.register_blueprint(produto_bp)
    

    return app

# Este bloco só será executado quando você rodar o script diretamente
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
    