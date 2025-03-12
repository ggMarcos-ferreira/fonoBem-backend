from flask_restful import Resource
from models.audio import AudioModel, db
from helpers.audio.upload import upload_file
import os

class Audio(Resource):
    def get(self, audio_id=None):
        if audio_id:
            audio = AudioModel.query.get(audio_id)
            if audio:
                return audio.json(), 200
            return {"message": "Audio não encontrado"}, 404
        audios = AudioModel.query.all()
        return [audio.json() for audio in audios], 200

    def post(self):
        # Realiza o upload do arquivo e salva localmente
        response = upload_file()
        if response[1] == 201:
            data = response[0]
            # Armazena informações do arquivo no banco de dados
            new_audio = AudioModel(filename=data['filename'], filepath=data['filepath'])
            db.session.add(new_audio)
            db.session.commit()
            return new_audio.json(), 201
        return response

    def delete(self, audio_id):
        # Deleta o áudio local e do banco de dados
        audio = AudioModel.query.get(audio_id)
        if audio:
            try:
                os.remove(audio.filepath)
                db.session.delete(audio)
                db.session.commit()
                return {"message": "Audio deletado com sucesso"}, 200
            except Exception as e:
                return {"message": f"Erro ao deletar áudio: {str(e)}"}, 500
        return {"message": "Audio não encontrado"}, 404