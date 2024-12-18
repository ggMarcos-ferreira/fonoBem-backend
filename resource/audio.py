from flask_restful import Resource
from models.audio import AudioModel, db
from audio.audios import AudioUpload
import os

audio_helper = AudioUpload()

class Audio(Resource):
    def get(self, audio_id=None):
        if audio_id:
            audio = AudioModel.query.get(audio_id)
            if audio:
                return audio.json(), 200
            return {"message": "Audio not found"}, 404

        audios = AudioModel.query.all()
        return [audio.json() for audio in audios], 200

    def post(self):
        # Realiza o upload do arquivo e salva localmente
        response = audio_helper.upload_file()
        if response[1] == 201:
            data = response[0].json
            # Armazena informações do arquivo no banco de dados
            new_audio = AudioModel(filename=data['filename'], filepath=data['filepath'])
            db.session.add(new_audio)
            db.session.commit()
        return response

    def delete(self, audio_id):
        # Deleta o áudio local e do banco de dados
        audio = AudioModel.query.get(audio_id)
        if audio:
            try:
                os.remove(audio.filepath)
                db.session.delete(audio)
                db.session.commit()
                return {"message": "Audio deleted successfully"}, 200
            except Exception as e:
                return {"message": f"Error deleting audio: {str(e)}"}, 500
        return {"message": "Audio not found"}, 404
