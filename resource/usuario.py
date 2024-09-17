from flask import request
from flask_restful import Resource
from models.usuario import UsuarioModel, db  # Importa o modelo

class Usuario(Resource):
    """
    Recurso para gerenciar os usuários.
    Implementa os métodos GET, POST, PUT e DELETE.
    """
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

        novo_usuario = UsuarioModel(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            numero_instituicao=dados.get('numero_instituicao')
        )
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
        usuario.numero_instituicao = dados.get('numero_instituicao', usuario.numero_instituicao)

        db.session.commit()
        return usuario.json(), 200

    def delete(self, usuario_id):
        usuario = UsuarioModel.query.filter_by(id=usuario_id).first()
        if not usuario:
            return {'message': 'Usuário não encontrado'}, 404

        db.session.delete(usuario)
        db.session.commit()
        return {'message': 'Usuário deletado'}, 200
