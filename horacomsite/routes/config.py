import mysql.connector
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:amarelo123*@localhost/horacom'

db = SQLAlchemy()


def get_db_config():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'amarelo123*',
        'database': 'horacom',
        'raise_on_warnings': True,
    }




def conectar_banco_de_dados():
    try:
        db_config = get_db_config()  # Obtendo os detalhes de configuração do banco de dados
        conexao = mysql.connector.connect(**db_config)  # Conectando ao banco de dados
        
        if conexao.is_connected():
            print("Conexão bem-sucedida ao banco de dados!")
            conexao.close()  # Fechando a conexão
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

# Chama a função para testar a conexão com o banco de dados
conectar_banco_de_dados()

