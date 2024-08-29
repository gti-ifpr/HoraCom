import mysql.connector
from config import db_get_config

try:
    conexao = mysql.connector.connect(**db_get_config())

    criar_tabela_SQL = """CREATE TABLE usuarios (
                        nome VARCHAR(100),
                        cpf VARCHAR(11),
                        tipo_usuario VARCHAR(100),
                        email VARCHAR(100),
                        senha VARCHAR(10)
                        )"""
    cursor = conexao.cursor()
    cursor.execute(criar_tabela_SQL)
    print("Tabela Usuarios criada com sucesso!")

    conexao.commit()
except mysql.connector.Error as erro:
    print("Falha ao criar tabela no MySQL: {}".format(erro))
finally:
    if conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão ao MySQL finalizada.")

try:
    conexao = mysql.connector.connect(**db_get_config())

    criar_tabela_SQL = """CREATE TABLE certificados (
                        email VARCHAR(100),
                        grupo VARCHAR(10),
                        opcao VARCHAR(10),
                        hora VARCHAR(10),
                        anexo VARBINARY(65000)
                        )"""
    cursor = conexao.cursor()
    cursor.execute(criar_tabela_SQL)
    print("Tabela Certificados criada com sucesso!")

    conexao.commit()
except mysql.connector.Error as erro:
    print("Falha ao criar tabela no MySQL: {}".format(erro))
finally:
    if conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão ao MySQL finalizada.")