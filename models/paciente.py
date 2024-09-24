from flask_restful import fields
from helpers.database import db # Importa a instância db

# Definindo o esquema de saída para o paciente
paciente_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'telefone': fields.String,
    'data_nascimento': fields.String,  # Data convertida para string
    'observacoes': fields.String,  
}

# Modelo do Paciente
class PacienteModel(db.Model):
    """
    Modelo para a tabela 'pacientes' no banco de dados.
    Contém os atributos: id, nome, email, telefone, data_nascimento, observacoes e senha.
    """
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(80), nullable=False)  # Nome do paciente
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email, deve ser único
    telefone = db.Column(db.String(20), nullable=False)  # Telefone do paciente
    data_nascimento = db.Column(db.Date, nullable=False)  # Data de nascimento do paciente
    observacoes = db.Column(db.Text, nullable=True)  # Observações sobre o paciente
    senha = db.Column(db.String(128), nullable=False)  # Senha do paciente

    def __repr__(self):
        """Retorna a representação textual do objeto."""
        return f"Paciente(nome={self.nome}, email={self.email}, telefone={self.telefone}, data_nascimento={self.data_nascimento})"

    def json(self):
        """Converte o objeto em um dicionário JSON."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'data_nascimento': str(self.data_nascimento),  # Convertendo para string
            'observacoes': self.observacoes,
            'senha': self.senha  # Incluindo o campo senha
        }
