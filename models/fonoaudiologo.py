from helpers.database import db # Importa a instância db

# Modelo do Fonoaudiólogo
class FonoaudiologoModel(db.Model):
    """
    Modelo para a tabela 'fonoaudiologos' no banco de dados.
    Contém os atributos: id, nome, email, telefone, numero_instituicao, senha.
    """
    __tablename__ = 'fonoaudiologos'

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(80), nullable=False)  # Nome do fonoaudiólogo
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email, deve ser único
    telefone = db.Column(db.String(20), nullable=False)  # Telefone do fonoaudiólogo
    numero_instituicao = db.Column(db.String(20), nullable=True)  # Número da instituição
    senha = db.Column(db.String(128), nullable=False)  # Senha do fonoaudiólogo

    def __repr__(self):
        """Retorna a representação textual do objeto."""
        return f"Fonoaudiologo(nome={self.nome}, email={self.email}, telefone={self.telefone}, numero_instituicao={self.numero_instituicao}, senha={self.senha})"

    def json(self):
        """Converte o objeto em um dicionário JSON."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'numero_instituicao': self.numero_instituicao,
            'senha': self.senha
        }
