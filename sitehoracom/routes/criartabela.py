import mysql.connector
from config import get_db_config

try:
    conexao = mysql.connector.connect(**get_db_config())
    cursor = conexao.cursor()

    criar_tabela_SQL = """CREATE TABLE usuarios (
                        nome VARCHAR(100),
                        cpf VARCHAR(11),
                        tipo_usuario INT(5),
                        email VARCHAR(100),
                        senha VARCHAR(10)
                        )"""

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
