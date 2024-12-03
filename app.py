import os
from flask import Flask
from helpers.database import db, migrate
from helpers.api import api, blueprint
from helpers.cors import cors
from resource.paciente import AudioUpload  # Recurso de upload

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/fono_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do diretório de uploads
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB

# Criar a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Inicializando extensões
db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)
api.init_app(app)  # Inicializa a API no app

# Registrando o blueprint
app.register_blueprint(blueprint)

# Adicionando o recurso de upload de áudio
api.add_resource(AudioUpload, '/upload_audio')

# Comentado: Use comandos de migração em vez de recriar tabelas diretamente
# with app.app_context():
#     db.drop_all()
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)