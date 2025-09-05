from flask import Flask
from extensions import db, mail, oauth
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Configurações do App
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ifome.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    # Inicializa as extensões
    db.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    # Registro do Google OAuth
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    # Registro do Facebook OAuth
    oauth.register(
            name='facebook',
            client_id=os.getenv('FACEBOOK_CLIENT_ID'),
            client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
            api_base_url='https://graph.facebook.com/v15.0/',
            access_token_url='https://graph.facebook.com/v15.0/oauth/access_token',
            authorize_url='https://www.facebook.com/v15.0/dialog/oauth',
            client_kwargs={'scope': 'email public_profile'},
    )

    # Importação e registro dos Blueprints
    from src.controllers.usuarios import usuarios_bp
    from src.controllers.home import home_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)