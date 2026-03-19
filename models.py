from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# ==============================
# TABELA DE USUÁRIOS
# ==============================
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # diretor, supervisor, desenvolvedor

    def __repr__(self):
        return f'<Usuario {self.username}>'


# ==============================
# TABELA DE EVENTOS / CONTRATOS
# ==============================
class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # evento ou contrato

    colaboradores = db.relationship('Colaborador', backref='evento', lazy=True)

    def __repr__(self):
        return f'<Evento {self.nome}>'


# ==============================
# TABELA DE COLABORADORES
# ==============================
class Colaborador(db.Model):
    __tablename__ = 'colaboradores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    cn = db.Column(db.String(50))  # campo adicional
    sexo = db.Column(db.String(10))
    valor_pagamento = db.Column(db.Float, nullable=False)
    pix = db.Column(db.String(100))
    banco = db.Column(db.String(100))
    profissao = db.Column(db.String(50), nullable=False)

    # 🔥 NOVO CAMPO ADICIONADO (SEM REMOVER NADA)
    foto = db.Column(db.String(255))

    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)

    presencas = db.relationship('Presenca', backref='colaborador', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Colaborador {self.nome}>'


# ==============================
# TABELA DE PRESENÇAS
# ==============================
class Presenca(db.Model):
    __tablename__ = 'presencas'

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'), nullable=False)
    data_presenca = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Presenca {self.data_presenca}>'
