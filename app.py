from flask import Flask, request
from flask_restful import Api
from models.usuario import db
from resource.usuario import Usuario 

# Inicializando a aplicação Flask
app = Flask(__name__)
api = Api(app)

# Configurando o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/fono_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy com o app
db.init_app(app)

# Criando as tabelas
with app.app_context():
    db.drop_all()  # Remover todas as tabelas (não usar em produção)
    db.create_all()  # Criar as tabelas

# Definindo as rotas da API
api.add_resource(Usuario, '/usuarios', '/usuarios/<int:usuario_id>')

if __name__ == '__main__':
    app.run(debug=True)
