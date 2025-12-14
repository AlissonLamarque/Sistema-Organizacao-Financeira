from flask import Flask, redirect, url_for
from .extensions import db

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'minha_chave_super_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:laboratorio@localhost/sistemafn'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from app.mercado.routes import mercado_bp
    app.register_blueprint(mercado_bp)
    
    @app.route('/')
    def root():
        return redirect(url_for('mercado.index'))
    
    return app