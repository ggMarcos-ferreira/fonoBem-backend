from flask import request
from flask_restful import Resource
from models.paciente import PacienteModel, db
from helpers.logging import logger

class Paciente(Resource):
    def get(self, paciente_id=None):
        if paciente_id:
            paciente = PacienteModel.query.get(paciente_id)
            if paciente:
                return paciente.json(), 200  # Usa o método json() do modelo
            return {'message': 'Paciente não encontrado'}, 404
        pacientes = PacienteModel.query.all()
        return [paciente.json() for paciente in pacientes], 200  # Retorna uma lista de JSON

    def post(self):
        dados = request.get_json()

        # Verifica se os campos obrigatórios estão presentes
        if not all(dados.get(field) for field in ['nome', 'email', 'telefone', 'senha']):
            logger.error("Dados obrigatórios não fornecidos.")
            return {'message': 'Nome, email, telefone e senha são obrigatórios'}, 400

        # Verifica se o email já está em uso
        if PacienteModel.query.filter_by(email=dados['email']).first():
            logger.warning(f"Email já está em uso: {dados['email']}")
            return {'message': 'Email já está em uso'}, 400

        # Cria o novo paciente
        novo_paciente = PacienteModel(
            nome=dados['nome'],
            email=dados['email'],
            telefone=dados['telefone'],
        )
        novo_paciente.set_senha(dados['senha'])  # Gera o hash da senha

        db.session.add(novo_paciente)
        db.session.commit()
        logger.info(f"Novo paciente adicionado: {novo_paciente.json()}")
        return novo_paciente.json(), 201