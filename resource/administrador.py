from flask import request
from flask_restful import Resource
from models.administrador import AdministradorModel, db  # Importa o modelo

class Administrador(Resource):
    """
    Recurso para gerenciar os administradores.
    Implementa os métodos GET, POST, PUT e DELETE.
    """
    def get(self, administrador_id=None):
        if administrador_id:
            administrador = AdministradorModel.query.filter_by(id=administrador_id).first()
            if administrador:
                return administrador.json(), 200
            return {'message': 'Administrador não encontrado'}, 404
        else:
            administradores = AdministradorModel.query.all()
            return [administrador.json() for administrador in administradores], 200

    def post(self):
        dados = request.get_json()
        if not dados.get('nome') or not dados.get('email') or not dados.get('telefone') or not dados.get('senha'):
            return {'message': 'Nome, email, telefone e senha são obrigatórios'}, 400

        if AdministradorModel.query.filter_by(email=dados['email']).first():
            return {'message': 'Email já está em uso'}, 400

        novo_administrador = AdministradorModel(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            senha=dados['senha']  
        )
        db.session.add(novo_administrador)
        db.session.commit()
        return novo_administrador.json(), 201

    def put(self, administrador_id):
        administrador = AdministradorModel.query.filter_by(id=administrador_id).first()
        if not administrador:
            return {'message': 'Administrador não encontrado'}, 404

        dados = request.get_json()
        administrador.nome = dados.get('nome', administrador.nome)
        administrador.email = dados.get('email', administrador.email)
        administrador.telefone = dados.get('telefone', administrador.telefone)
        administrador.senha = dados.get('senha', administrador.senha) 

        db.session.commit()
        return administrador.json(), 200

    def delete(self, administrador_id):
        administrador = AdministradorModel.query.filter_by(id=administrador_id).first()
        if not administrador:
            return {'message': 'Administrador não encontrado'}, 404

        db.session.delete(administrador)
        db.session.commit()
        return {'message': 'Administrador deletado'}, 200
