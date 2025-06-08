from flask import Flask
from flask_cors import CORS
from backend.routes.api import api_bp
from dotenv import load_dotenv
import os

def create_app():
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()
    
    app = Flask(__name__)
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
    app.config['DATABASE_NAME'] = os.getenv('DATABASE_NAME')
    app.config['COLLECTION_NAME'] = os.getenv('COLLECTION_NAME')
    
    # Habilitar CORS para permitir requisições do frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Registrar blueprint de rotas
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)