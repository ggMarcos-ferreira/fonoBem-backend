import os
from flask import Flask
from helpers.database import db, migrate
from helpers.api import api, blueprint
from helpers.cors import cors
from resource.audio import Audio  

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/fono_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do diretório de uploads
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB

# Cria a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Inicializando extensões
db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)
api.init_app(app)  

# Registrando o blueprint
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)