from flask_restful import Resource, reqparse
from flask import request, current_app
import os
from werkzeug.utils import secure_filename

class AudioUpload(Resource):  # Certifique-se de herdar de Resource
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part"}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {"message": "No selected file"}, 400
        
        # Validando o tipo do arquivo (opcional)
        allowed_extensions = {'mp3', 'wav', 'ogg'}
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return {"message": "File type not allowed"}, 400

        # Salvando o arquivo
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        return {"message": "File uploaded successfully", "filename": filename, "filepath": file_path}, 201
