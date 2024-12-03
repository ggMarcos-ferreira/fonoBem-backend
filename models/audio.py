from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AudioModel(db.Model):
    __tablename__ = 'audios'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Audio {self.filename}>"

    def json(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "filepath": self.filepath
        }