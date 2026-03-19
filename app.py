from flask import Flask
from config import Config
from models import db, Usuario, Evento
from routes import init_routes
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os

# ==============================
# INICIALIZAÇÃO DO APP
# ==============================
app = Flask(__name__)
app.config.from_object(Config)

# ==============================
# BANCO DE DADOS
# ==============================
db.init_app(app)

# ==============================
# LOGIN MANAGER
# ==============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# ==============================
# CRIAÇÃO AUTOMÁTICA DO BANCO
# ==============================
def criar_dados_iniciais():
    db.create_all()

    # ==============================
    # USUÁRIOS PADRÃO
    # ==============================
    if not Usuario.query.first():
        usuarios = [
            Usuario(
                username='diretor',
                password=generate_password_hash('123456'),
                role='diretor'
            ),
            Usuario(
                username='supervisor',
                password=generate_password_hash('123456'),
                role='supervisor'
            ),
            Usuario(
                username='dev',
                password=generate_password_hash('123456'),
                role='desenvolvedor'
            )
        ]

        for u in usuarios:
            db.session.add(u)

        print("✔ Usuários padrão criados")

    # ==============================
    # EVENTOS / CONTRATOS PADRÃO
    # ==============================
    if not Evento.query.first():
        eventos = [
            Evento(nome='Supermercado ABC', tipo='contrato'),
            Evento(nome='Prefeitura de Queimados', tipo='contrato'),
            Evento(nome='Evento Show Rock', tipo='evento')
        ]

        for e in eventos:
            db.session.add(e)

        print("✔ Eventos padrão criados")

    db.session.commit()


# ==============================
# INICIALIZAÇÃO DAS ROTAS
# ==============================
init_routes(app)

# 🔥 CORREÇÃO CRÍTICA (EXECUTA NO RENDER)
with app.app_context():
    criar_dados_iniciais()


# ==============================
# EXECUÇÃO DO APP
# ==============================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
