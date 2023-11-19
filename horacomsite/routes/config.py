from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import inspect

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

# Exemplo de como obter as tabelas do banco de dados
def get_tables():
    config = db_get_config()

    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
    
    return tables

if __name__ == '__main__':
    print(get_tables())


def get_tables():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        return tables

if __name__ == "__main__":
    tables = get_tables()
    print("Tabelas no banco de dados:")
    for table in tables:
        print(table)

class Certificados(db.Model):
    __tablename__ = 'certificados'
    email = db.Column(db.String(100), primary_key=True)
    grupo = db.Column(db.String(10))
    opcao = db.Column(db.String(10))
    hora = db.Column(db.String(10))
    anexo = db.Column(db.LargeBinary)

def get_table_content(table_name):
    with app.app_context():
        rows = db.session.query(Certificados).all()
        return rows

if __name__ == "__main__":
    table_content = get_table_content('certificados')
    print("Conteúdo da tabela 'certificados':")
    for row in table_content:
        print(row.email, row.grupo, row.opcao, row.hora, row.anexo)       