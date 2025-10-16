from flask import Flask
from models import db
from routes.base import main_bp

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'minha_chave_super_secreta'
    # IMPORTANTE: Verifique se o nome do seu banco de dados é 'sistemadb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:laboratorio@localhost/sistemadb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa o DB com a aplicação
    db.init_app(app)

    # --- LINHA CRÍTICA ---
    # Registra o Blueprint para que a aplicação conheça as rotas
    app.register_blueprint(main_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

