from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate
from helpers.api import api, blueprint
from helpers.cors import cors
from resources.paciente import AudioUpload  # Importe o novo recurso

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configurando a API
api = Api(app)

# Configurando o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/fono_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do upload de arquivos
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Pasta para armazenar os arquivos
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads

# Inicializando o SQLAlchemy com o app
db.init_app(app)

# Inicializando a migração com a aplicação e o banco de dados
migrate.init_app(app, db)

# Inicializando o CORS com o app
cors.init_app(app)

# Registrando o blueprint
app.register_blueprint(blueprint)

# Adicionando o recurso de upload de áudio à API
api.add_resource(AudioUpload, '/upload_audio')

# Criando as tabelas 
with app.app_context():
    db.drop_all()  # Remover todas as tabelas
    db.create_all()  # Criar as tabelas

if __name__ == '__main__':
    app.run(debug=True)
