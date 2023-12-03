from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:amarelo123*@localhost/HoraCom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        # Consulta SQL para somar as horas associadas a este usuário nos certificados
        result = db.session.query(func.sum(Certificados.hora)).filter_by(email=email).scalar()
        return result or 0.0

if __name__ == '__main__':
    tables = get_tables()
    print("Tabelas no banco de dados:")
    for table in tables:
        print(table)

    table_content = get_table_content('certificados')
    print("Conteúdo da tabela 'certificados':")
    for row in table_content:
        print(row.email, row.grupo, row.opcao, row.hora, row.anexo)

    # Exemplo de como usar a função de soma
    email_exemplo = 'ferteixeira555@gmail.com'
    soma_horas = somar_horas_certificados(email_exemplo)
    print(f"Soma das horas para o email {email_exemplo}: {soma_horas}")
