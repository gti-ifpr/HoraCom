import mysql.connector
from config import get_db_config

#ESSA FUNÇÃO DEU CERTO DIRETAMENTE DE PYTHON PARA MYSQL TEMOS QUE FAZER A LOGICA DO HTML 

conexao = mysql.connector.connect(**get_db_config())
    # Função para inserir um certificado na tabela Certificados do MySQL
def anexar(id_aluno, grupo, opcao, quantidade_horas):
    try:
       
        cursor = conexao.cursor()

        # Inserir os dados na tabela Certificados
        query = "INSERT INTO Certificados (id_aluno, grupo, opcao, quantidade_horas) VALUES (%s, %s, %s, %s)"
        values = (id_aluno, grupo, opcao, quantidade_horas)
        cursor.execute(query, values)

        # Commit para salvar as alterações
        conexao.commit()
        print("Certificado inserido com sucesso!")
    except mysql.connector.Error as e:
        print("Erro ao inserir certificado:", str(e))
    finally:
        # Fechar a conexão com o banco de dados
        conexao.close()
   # return render_template('anexar.html')


# Exemplo de uso da função
anexar(1, 'g1', 'Opção 1', 30.5)


