from flask import request, jsonify
from flask_restful import Resource
import os
from werkzeug.utils import secure_filename
from helpers.logging import logger

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}  # Tipos de arquivos permitidos

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AudioUpload(Resource):
    """
    Recurso para fazer o upload de áudios.
    """
    def post(self):
        # Verifica se o arquivo foi enviado
        if 'audio' not in request.files:
            logger.error("Nenhum arquivo enviado.")
            return {'message': 'Nenhum arquivo enviado'}, 400

        file = request.files['audio']
        
        if file.filename == '':
            logger.error("Nenhum arquivo selecionado.")
            return {'message': 'Nenhum arquivo selecionado'}, 400
        
        # Verifica se a extensão do arquivo é permitida
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Evita problemas de nome de arquivo
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Salva o arquivo no servidor
            file.save(file_path)
            logger.info(f"Arquivo {filename} salvo com sucesso em {file_path}.")
            
            return {'message': 'Arquivo enviado com sucesso', 'file_path': file_path}, 201

        logger.warning("Tipo de arquivo não permitido.")
        return {'message': 'Tipo de arquivo não permitido'}, 400
