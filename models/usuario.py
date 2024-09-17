from flask_sqlalchemy import SQLAlchemy

# Inicializando o SQLAlchemy 
db = SQLAlchemy()

# Modelo do Usuário
class UsuarioModel(db.Model):
    """
    Modelo para a tabela 'usuarios' no banco de dados.
    Contém os atributos: id, nome, email, telefone, numero_instituicao.
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(80), nullable=False)  # Nome do usuário
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email, deve ser único
    telefone = db.Column(db.String(20), nullable=False)  # Telefone do usuário
    numero_instituicao = db.Column(db.String(20), nullable=True)  # Número da instituição

    def __repr__(self):
        """Retorna a representação textual do objeto."""
        return f"Usuario(nome={self.nome}, email={self.email}, telefone={self.telefone}, numero_instituicao={self.numero_instituicao})"

    def json(self):
        """Converte o objeto em um dicionário JSON."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'numero_instituicao': self.numero_instituicao
        }