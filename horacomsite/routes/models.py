from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Certificados(db.Model):
    __tablename__ = 'certificados'
    email = db.Column(db.String(100), primary_key=True)
    grupo = db.Column(db.String(10))
    opcao = db.Column(db.String(10))
    hora = db.Column(db.String(10))
    anexo = db.Column(db.LargeBinary)

class User(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)

    # Adicione um relacionamento com a tabela RegistroHoras
    registros_horas = db.relationship('RegistroHoras', backref='usuario', lazy='dynamic')

    def __init__(self, email, senha, tipo_usuario):
        self.email = email
        self.senha_hash = generate_password_hash(senha)
        self.tipo_usuario = tipo_usuario

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

   