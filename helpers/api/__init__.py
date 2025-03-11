from flask_restful import Api
from flask import Blueprint

# Importando os recursos
from resource.administrador import Administrador
from resource.fonoaudiologo import Fonoaudiologo
from resource.paciente import Paciente
from resource.audio import Audio

# Criando um blueprint para a API
blueprint = Blueprint('api', __name__)

# Inicializando a API com o prefixo '/api'
api = Api(blueprint, prefix="/api")

# Definindo as rotas da API
api.add_resource(Fonoaudiologo, '/fonoaudiologos', '/fonoaudiologos/<int:fonoaudiologo_id>')  
api.add_resource(Administrador, '/administradores', '/administradores/<int:administrador_id>')
api.add_resource(Paciente, '/pacientes', '/pacientes/<int:paciente_id>')
api.add_resource(Audio, '/audios', '/audios/<int:audio_id>')