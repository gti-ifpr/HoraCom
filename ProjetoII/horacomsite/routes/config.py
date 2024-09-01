from flask import Flask, render_template,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:amarelo123*@localhost/HoraCom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key ='CamilaFer123*'
db = SQLAlchemy(app)

def db_get_config():
    return {
        'user': 'root',
        'password': 'amarelo123*',
        'host': 'localhost',
        'database': 'HoraCom',
        'port': '3306',
    }

class Certificados(db.Model):
    __tablename__ = 'certificados'
    email = db.Column(db.String(100), primary_key=True)
    grupo = db.Column(db.String(10))
    opcao = db.Column(db.String(10))
    hora = db.Column(db.String(10))
    anexo = db.Column(db.LargeBinary)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    email = db.Column(db.String(255), primary_key=True)
    nome = db.Column(db.String(255))

def get_nome_usuario_logado():
    if session and 'usuario_nome' in session:
        nome_usuario = session['usuario_nome']
        print(f"Nome do usuário na sessão: {nome_usuario}")
        return nome_usuario
    return None

def get_tables():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        return tables


def get_table_content(table_name):
    with app.app_context():
        rows = db.session.query(Certificados).all()
        return rows

def somar_horas_certificados(email):
    with app.app_context():
        result = db.session.query(func.sum(Certificados.hora)).filter_by(email=email).scalar()
        return result or 0.0

if __name__ == '__main__':
    with app.app_context():
        nome_usuario = get_nome_usuario_logado()
        print(f"Nome do usuário logado: {nome_usuario}")

        tables = get_tables()
        print("Tabelas no banco de dados:")
        for table in tables:
            print(table)

        table_content = get_table_content('certificados')
        print("Conteúdo da tabela 'certificados':")
        for row in table_content:
            print(row.email, row.grupo, row.opcao, row.hora, row.anexo)

        email_exemplo = 'ferteixeira555@gmail.com'
        soma_horas = somar_horas_certificados(email_exemplo)
        print(f"Soma das horas para o email {email_exemplo}: {soma_horas}")

        resultados = (
            db.session.query(Certificados.grupo, Certificados.opcao, Certificados.hora, Certificados.anexo, Usuario.nome)
            .join(Usuario, Certificados.email == Usuario.email)
            .filter(Certificados.email == email_exemplo)
            .all()
        )
        print("Resultados da consulta:")
        for resultado in resultados:
            print(resultado)

