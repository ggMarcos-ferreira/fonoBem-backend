from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# Inicializando a aplicação Flask
app = Flask(__name__)
api = Api(app)

# Configurando o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/fono_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy com a aplicação Flask
db = SQLAlchemy(app)

# Modelo do Usuário
class UsuarioModel(db.Model):
    """
    Modelo para a tabela 'usuarios' no banco de dados.
    Contém os atributos: id, nome, email, telefone.
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(80), nullable=False)  # Nome do usuário
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email, deve ser único
    telefone = db.Column(db.String(20), nullable=False)  # Telefone do usuário

    def __repr__(self):
        """Retorna a representação textual do objeto."""
        return f"Usuario(nome={self.nome}, email={self.email}, telefone={self.telefone})"

    def json(self):
        """Converte o objeto em um dicionário JSON."""
        return {'id': self.id, 'nome': self.nome, 'email': self.email, 'telefone': self.telefone}

# Criação das tabelas no banco de dados
with app.app_context():
    db.drop_all()  # Remove todas as tabelas (não usar em produção)
    db.create_all()  # Cria as tabelas com base nos modelos

class Usuario(Resource):
    """
    Recurso para gerenciar os usuários.
    Implementa os métodos GET, POST, PUT e DELETE.
    """
    def get(self, usuario_id=None):
        """
        Retorna a lista de usuários ou um usuário específico por ID.
        """
        if usuario_id:
            usuario = UsuarioModel.query.filter_by(id=usuario_id).first()
            if usuario:
                return usuario.json(), 200
            return {'message': 'Usuário não encontrado'}, 404
        else:
            usuarios = UsuarioModel.query.all()
            return [usuario.json() for usuario in usuarios], 200

    def post(self):
        """
        Cria um novo usuário com base nos dados fornecidos.
        Verifica se o email já está em uso.
        """
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
        """
        Atualiza os dados de um usuário existente.
        Verifica se o usuário existe, caso contrário retorna erro 404.
        """
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
        """
        Remove um usuário existente.
        Verifica se o usuário existe, caso contrário retorna erro 404.
        """
        usuario = UsuarioModel.query.filter_by(id=usuario_id).first()
        if not usuario:
            return {'message': 'Usuário não encontrado'}, 404

        db.session.delete(usuario)
        db.session.commit()
        return {'message': 'Usuário deletado'}, 200

class Index(Resource):
    """
    Recurso para a rota raiz que retorna a versão do Flask.
    """
    def get(self):
        import flask
        return {'version': flask.__version__}, 200

# Definindo as rotas da API
api.add_resource(Usuario, '/usuarios', '/usuarios/<int:usuario_id>')
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True)
