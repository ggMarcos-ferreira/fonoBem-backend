from helpers.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class PacienteModel(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(256), nullable=False)  # Senha será armazenada como hash

    def __repr__(self):
        return f"Paciente(nome={self.nome}, email={self.email}, telefone={self.telefone})"

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
        }

    def set_senha(self, senha):
        """Gera o hash da senha e armazena no banco de dados."""
        self.senha = generate_password_hash(senha)

    def check_senha(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha, senha)