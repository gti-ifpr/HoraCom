import mysql.connector

#ESSA FUNÇÃO DEU CERTO DIRETAMENTE DE PYTHON PARA MYSQL TEMOS QUE FAZER A LOGICA DO HTML 

# Função para inserir um certificado na tabela Certificados do MySQL
def inserir_certificado(id_aluno, grupo, opcao, quantidade_horas):
    try:
        # Conectar ao banco de dados MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='amarelo123*',
            database='horacom'
        )
        cursor = conn.cursor()

        # Inserir os dados na tabela Certificados
        query = "INSERT INTO Certificados (id_aluno, grupo, opcao, quantidade_horas) VALUES (%s, %s, %s, %s)"
        values = (id_aluno, grupo, opcao, quantidade_horas)
        cursor.execute(query, values)

        # Commit para salvar as alterações
        conn.commit()
        print("Certificado inserido com sucesso!")
    except mysql.connector.Error as e:
        print("Erro ao inserir certificado:", str(e))
    finally:
        # Fechar a conexão com o banco de dados
        conn.close()

# Exemplo de uso da função
inserir_certificado(1, 'g1', 'Opção 1', 30.5)


