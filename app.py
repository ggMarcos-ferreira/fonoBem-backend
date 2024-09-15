from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# Inicializando a aplicação Flask
app = Flask(__name__)
api = Api(app)

# Configurando o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/fono_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Usuário
class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Usuario(nome={self.nome}, email={self.email}, telefone={self.telefone})"

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email, 'telefone': self.telefone}

# Criando a tabela no banco de dados
with app.app_context():
    db.drop_all()  # Remove todas as tabelas
    db.create_all()  # Cria as tabelas novamente com a nova estrutura

# Definindo o recurso Usuario
class Usuario(Resource):
    def get(self, usuario_id=None):
        if usuario_id:
            usuario = UsuarioModel.query.filter_by(id=usuario_id).first()
            if usuario:
                return usuario.json(), 200
            return {'message': 'Usuário não encontrado'}, 404
        else:
            usuarios = UsuarioModel.query.all()
            return [usuario.json() for usuario in usuarios], 200

    def post(self):
        dados = request.get_json()
        if not dados.get('nome') or not dados.get('email') or not dados.get('telefone'):
            return {'message': 'Nome, email e telefone são obrigatórios'}, 400

        if UsuarioModel.query.filter_by(email=dados['email']).first():
            return {'message': 'Email já está em uso'}, 400

        novo_usuario = UsuarioModel(nome=dados['nome'], email=dados['email'], telefone=dados['telefone'])
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario.json(), 201

    def put(self, usuario_id):
        usuario = UsuarioModel.query.filter_by(id=usuario_id).first()
        if not usuario:
            return {'message': 'Usuário não encontrado'}, 404

        dados = request.get_json()
        usuario.nome = dados.get('nome', usuario.nome)
        usuario.email = dados.get('email', usuario.email)
        usuario.telefone = dados.get('telefone', usuario.telefone)

        db.session.commit()
        return usuario.json(), 200

    def delete(self, usuario_id):
        usuario = UsuarioModel.query.filter_by(id=usuario_id).first()
        if not usuario:
            return {'message': 'Usuário não encontrado'}, 404

        db.session.delete(usuario)
        db.session.commit()
        return {'message': 'Usuário deletado'}, 200

class Index(Resource):
    def get(self):
        import flask
        return {'version': flask.__version__}, 200
    
# Adicionando o resource Usuario à API
api.add_resource(Usuario, '/usuarios', '/usuarios/<int:usuario_id>')
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True)
