from flask import Flask
from flask_restful import Api
from helpers.database import db  
from helpers.api import api, blueprint
from helpers.cors import cors

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configurando a API
api = Api(app)

# Configurando o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/fono_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy com o app
db.init_app(app)

# Inicializando a API
api.init_app(app)

# Inicializando o CORS com o app
cors.init_app(app)

# Registrando o blueprint
app.register_blueprint(blueprint)

# Criando as tabelas 
with app.app_context():
    db.drop_all()  # Remover todas as tabelas
    db.create_all()  # Criar as tabelas

if __name__ == '__main__':
    app.run(debug=True) 
