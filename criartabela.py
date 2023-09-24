import mysql.connector
import config

try:
    conexao = mysql.connector.connect(**config.get_db_config())

    criar_tabela_SQL = """ CREATE TABLE aluno (
                        nome varchar(100) NOT NULL,
                        cpf varchar(11) NOT NULL,
                        tipo_usuario int(5),
                        email varchar(100),
                        senha varchar(10)
                        )"""

    cursor = conexao.cursor()
    cursor.execute(criar_tabela_SQL)
    print("Tabela Alunos criada com sucesso!")

    conexao.commit()
except mysql.connector.Error as erro:
        print("Falha ao criar tabela no MySQL: ()".format(erro))

finally:
    if(conexao.is_connected()):
        cursor.close()
        conexao.close()
        print("Conexão ao MySQL finalizar.")