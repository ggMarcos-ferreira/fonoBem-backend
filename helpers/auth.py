from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from models.paciente import PacienteModel
from models.fonoaudiologo import FonoaudiologoModel

class Login(Resource):
    def post(self):
        # Recebe os dados do corpo da requisição
        dados = request.get_json()
        email = dados.get('email')
        senha = dados.get('senha')

        # Verifica se é um paciente
        paciente = PacienteModel.query.filter_by(email=email).first()
        if paciente and paciente.check_senha(senha):
            # Gera o token JWT para o paciente
            token = jwt.encode({
                'id': paciente.id,
                'tipo': 'paciente',  # Adiciona o tipo de usuário
                'exp': datetime.utcnow() + timedelta(hours=1)  # Token expira em 1 hora
            }, 'chave_secreta', algorithm='HS256')
            return {'token': token}, 200

        # Verifica se é um fonoaudiólogo
        fonoaudiologo = FonoaudiologoModel.query.filter_by(email=email).first()
        if fonoaudiologo and fonoaudiologo.check_senha(senha):
            # Gera o token JWT para o fonoaudiólogo
            token = jwt.encode({
                'id': fonoaudiologo.id,
                'tipo': 'fonoaudiologo',  # Adiciona o tipo de usuário
                'exp': datetime.utcnow() + timedelta(hours=1)  # Token expira em 1 hora
            }, 'chave_secreta', algorithm='HS256')
            return {'token': token}, 200
          
        return {'message': 'Email ou senha inválidos'}, 401