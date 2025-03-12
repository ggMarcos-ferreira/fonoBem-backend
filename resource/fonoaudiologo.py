from flask import request
from flask_restful import Resource
from models.fonoaudiologo import FonoaudiologoModel, db
from helpers.logging import logger

class Fonoaudiologo(Resource):
    def get(self, fonoaudiologo_id=None):
        if fonoaudiologo_id:
            fonoaudiologo = FonoaudiologoModel.query.get(fonoaudiologo_id)
            if fonoaudiologo:
                return fonoaudiologo.json(), 200  # Usa o método json() do modelo
            return {'message': 'Fonoaudiólogo não encontrado'}, 404
        fonoaudiologos = FonoaudiologoModel.query.all()
        return [fonoaudiologo.json() for fonoaudiologo in fonoaudiologos], 200  # Retorna uma lista de JSON

    def post(self):
        dados = request.get_json()

        # Verifica se os campos obrigatórios estão presentes
        if not all(dados.get(field) for field in ['nome', 'email', 'telefone', 'senha']):
            logger.error("Dados obrigatórios não fornecidos.")
            return {'message': 'Nome, email, telefone e senha são obrigatórios'}, 400

        # Verifica se o email já está em uso
        if FonoaudiologoModel.query.filter_by(email=dados['email']).first():
            logger.warning(f"Email já está em uso: {dados['email']}")
            return {'message': 'Email já está em uso'}, 400

        # Cria o novo fonoaudiólogo
        novo_fonoaudiologo = FonoaudiologoModel(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            numero_instituicao=dados.get('numero_instituicao'),
        )
        novo_fonoaudiologo.set_senha(dados['senha'])  # Gera o hash da senha

        db.session.add(novo_fonoaudiologo)
        db.session.commit()
        logger.info(f"Novo fonoaudiólogo adicionado: {novo_fonoaudiologo.json()}")
        return novo_fonoaudiologo.json(), 201