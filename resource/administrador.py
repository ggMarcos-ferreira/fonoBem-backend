from flask import request
from flask_restful import Resource, marshal_with
from models.administrador import AdministradorModel, db, administrador_fields  # Importa o modelo e os fields
from helpers.logging import logger

class Administrador(Resource):
    """
    Recurso para gerenciar os administradores.
    Implementa os métodos GET, POST, PUT e DELETE.
    """
    
    @marshal_with(administrador_fields)
    def get(self, administrador_id=None):
        if administrador_id:
            administrador = AdministradorModel.query.filter_by(id=administrador_id).first()
            if administrador:
                logger.info(f"Administrador encontrado: {administrador.json()}")
                return administrador, 200
            logger.warning(f"Administrador não encontrado: ID {administrador_id}")
            return {'message': 'Administrador não encontrado'}, 404
        else:
            administradores = AdministradorModel.query.all()
            logger.info("Retornando todos os administradores.")
            return administradores, 200

    @marshal_with(administrador_fields)
    def post(self):
        dados = request.get_json()
        if not (dados.get('nome') and dados.get('email') and 
                dados.get('telefone') and dados.get('senha')):
            logger.error("Dados obrigatórios não fornecidos.")
            return {'message': 'Nome, email, telefone e senha são obrigatórios'}, 400

        if AdministradorModel.query.filter_by(email=dados['email']).first():
            logger.warning(f"Email já está em uso: {dados['email']}")
            return {'message': 'Email já está em uso'}, 400

        novo_administrador = AdministradorModel(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            senha=dados['senha']
        )
        db.session.add(novo_administrador)
        db.session.commit()
        logger.info(f"Novo administrador adicionado: {novo_administrador.json()}")
        return novo_administrador, 201

    @marshal_with(administrador_fields) 
    def put(self, administrador_id):
        administrador = AdministradorModel.query.filter_by(id=administrador_id).first()
        if not administrador:
            logger.warning(f"Administrador não encontrado para atualização: ID {administrador_id}")
            return {'message': 'Administrador não encontrado'}, 404

        dados = request.get_json()
        administrador.nome = dados.get('nome', administrador.nome)
        administrador.email = dados.get('email', administrador.email)
        administrador.telefone = dados.get('telefone', administrador.telefone)
        administrador.senha = dados.get('senha', administrador.senha)

        db.session.commit()
        logger.info(f"Administrador atualizado: {administrador.json()}")
        return administrador, 200 

    def delete(self, administrador_id):
        administrador = AdministradorModel.query.filter_by(id=administrador_id).first()
        if not administrador:
            logger.warning(f"Tentativa de deletar administrador não encontrado: ID {administrador_id}")
            return {'message': 'Administrador não encontrado'}, 404

        db.session.delete(administrador)
        db.session.commit()
        logger.info(f"Administrador deletado: ID {administrador_id}")
        return {'message': 'Administrador deletado'}, 200
