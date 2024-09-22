from flask import request
from flask_restful import Resource
from models.fonoaudiologo import FonoaudiologoModel, db  # Importa o modelo

class Fonoaudiologo(Resource):
    """
    Recurso para gerenciar os fonoaudiólogos.
    Implementa os métodos GET, POST, PUT e DELETE.
    """
    def get(self, fonoaudiologo_id=None):
        if fonoaudiologo_id:
            fonoaudiologo = FonoaudiologoModel.query.filter_by(id=fonoaudiologo_id).first()
            if fonoaudiologo:
                return fonoaudiologo.json(), 200
            return {'message': 'Fonoaudiólogo não encontrado'}, 404
        else:
            fonoaudiologos = FonoaudiologoModel.query.all()
            return [fonoaudiologo.json() for fonoaudiologo in fonoaudiologos], 200

    def post(self):
        dados = request.get_json()
        if not dados.get('nome') or not dados.get('email') or not dados.get('telefone') or not dados.get('senha'):
            return {'message': 'Nome, email, telefone e senha são obrigatórios'}, 400

        if FonoaudiologoModel.query.filter_by(email=dados['email']).first():
            return {'message': 'Email já está em uso'}, 400

        novo_fonoaudiologo = FonoaudiologoModel(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            numero_instituicao=dados.get('numero_instituicao'),
            senha=dados['senha'] 
        )
        db.session.add(novo_fonoaudiologo)
        db.session.commit()
        return novo_fonoaudiologo.json(), 201

    def put(self, fonoaudiologo_id):
        fonoaudiologo = FonoaudiologoModel.query.filter_by(id=fonoaudiologo_id).first()
        if not fonoaudiologo:
            return {'message': 'Fonoaudiólogo não encontrado'}, 404

        dados = request.get_json()
        fonoaudiologo.nome = dados.get('nome', fonoaudiologo.nome)
        fonoaudiologo.email = dados.get('email', fonoaudiologo.email)
        fonoaudiologo.telefone = dados.get('telefone', fonoaudiologo.telefone)
        fonoaudiologo.numero_instituicao = dados.get('numero_instituicao', fonoaudiologo.numero_instituicao)
        fonoaudiologo.senha = dados.get('senha', fonoaudiologo.senha)

        db.session.commit()
        return fonoaudiologo.json(), 200

    def delete(self, fonoaudiologo_id):
        fonoaudiologo = FonoaudiologoModel.query.filter_by(id=fonoaudiologo_id).first()
        if not fonoaudiologo:
            return {'message': 'Fonoaudiólogo não encontrado'}, 404

        db.session.delete(fonoaudiologo)
        db.session.commit()
        return {'message': 'Fonoaudiólogo deletado'}, 200
