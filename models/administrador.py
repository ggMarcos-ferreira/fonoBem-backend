from helpers.database import db # Importa a instância db

# Modelo do Administrador
class AdministradorModel(db.Model):
    """
    Modelo para a tabela 'administradores' no banco de dados.
    Contém os atributos: id, nome, email, telefone, senha.
    """
    __tablename__ = 'administradores'

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(80), nullable=False)  # Nome do administrador
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email, deve ser único
    telefone = db.Column(db.String(20), nullable=False)  # Telefone do administrador
    senha = db.Column(db.String(128), nullable=False)  # Senha do administrador

    def __repr__(self):
        """Retorna a representação textual do objeto."""
        return f"Administrador(nome={self.nome}, email={self.email}, telefone={self.telefone}, senha={self.senha})"

    def json(self):
        """Converte o objeto em um dicionário JSON."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'senha': self.senha
        }
