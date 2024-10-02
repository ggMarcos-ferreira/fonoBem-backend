from flask import request
from flask_restful import Resource, marshal_with
from models.paciente import PacienteModel, db, paciente_fields  # Importa o modelo e os fields
from helpers.logging import logger

class Paciente(Resource):
    """
    Recurso para gerenciar os pacientes.
    Implementa os métodos GET, POST, PUT e DELETE.
    """
    
    @marshal_with(paciente_fields)
    def get(self, paciente_id=None):
        if paciente_id:
            paciente = PacienteModel.query.filter_by(id=paciente_id).first()
            if paciente:
                logger.info(f"Paciente encontrado: {paciente.json()}")
                return paciente, 200
            logger.warning(f"Paciente não encontrado: ID {paciente_id}")
            return {'message': 'Paciente não encontrado'}, 404
        else:
            pacientes = PacienteModel.query.all()
            logger.info("Retornando todos os pacientes.")
            return pacientes, 200

    @marshal_with(paciente_fields)
    def post(self):
        dados = request.get_json()
        # Verifica se os campos obrigatórios estão presentes
        if not all(dados.get(field) for field in ['nome', 'email', 'telefone', 'senha']):
            logger.error("Dados obrigatórios não fornecidos.")
            return {'message': 'Nome, email, telefone, data de nascimento e senha são obrigatórios'}, 400

        # Verifica se o email já está em uso
        if PacienteModel.query.filter_by(email=dados['email']).first():
            logger.warning(f"Email já está em uso: {dados['email']}")
            return {'message': 'Email já está em uso'}, 400

        novo_paciente = PacienteModel(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
            senha=dados['senha'] 
        )
        db.session.add(novo_paciente)
        db.session.commit()
        logger.info(f"Novo paciente adicionado: {novo_paciente.json()}")
        return novo_paciente, 201

    @marshal_with(paciente_fields)
    def put(self, paciente_id):
        paciente = PacienteModel.query.filter_by(id=paciente_id).first()
        if not paciente:
            logger.warning(f"Paciente não encontrado para atualização: ID {paciente_id}")
            return {'message': 'Paciente não encontrado'}, 404

        dados = request.get_json()
        paciente.nome = dados.get('nome', paciente.nome)
        paciente.email = dados.get('email', paciente.email)
        paciente.telefone = dados.get('telefone', paciente.telefone)
        paciente.data_nascimento = dados.get('data_nascimento', paciente.data_nascimento)
        paciente.senha = dados.get('senha', paciente.senha)

        db.session.commit()
        logger.info(f"Paciente atualizado: {paciente.json()}")
        return paciente, 200

    def delete(self, paciente_id):
        paciente = PacienteModel.query.filter_by(id=paciente_id).first()
        if not paciente:
            logger.warning(f"Tentativa de deletar paciente não encontrado: ID {paciente_id}")
            return {'message': 'Paciente não encontrado'}, 404

        db.session.delete(paciente)
        db.session.commit()
        logger.info(f"Paciente deletado: ID {paciente_id}")
        return {'message': 'Paciente deletado'}, 200
