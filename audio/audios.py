import os
from flask import request, jsonify
from werkzeug.utils import secure_filename

class AudioUpload:
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

    def __init__(self):
        # Certifique-se de que a pasta de uploads existe
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)

    def allowed_file(self, filename):
        # Verifica se o arquivo tem uma extensão permitida
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_file(self):
        # Valida a presença do arquivo na requisição
        if 'file' not in request.files:
            return jsonify({"message": "No file part in the request"}), 400
        
        file = request.files['file']

        # Verifica se um arquivo foi selecionado
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400

        # Valida a extensão do arquivo
        if not self.allowed_file(file.filename):
            return jsonify({"message": "File type not allowed"}), 400

        # Salva o arquivo localmente
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.UPLOAD_FOLDER, filename)
        file.save(filepath)

        return jsonify({"message": "File uploaded successfully", "filename": filename, "filepath": filepath}), 201
