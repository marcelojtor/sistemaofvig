import os

# Caminho absoluto do diretório base
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Chave secreta para sessões (IMPORTANTE para produção trocar por algo mais seguro)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-super-segura'

    # Configuração do banco SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database.db')

    # Evita warning desnecessário do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração para Flask-Login
    SESSION_TYPE = 'filesystem'


# Configuração de porta para Render
class RenderConfig(Config):
    PORT = int(os.environ.get("PORT", 5000))
