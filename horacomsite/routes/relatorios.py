import mysql.connector



#ESSA FUNÇÃO TESTADA DIRETO NO MYSQL DEU CERTO 

def gerar_relatorio_certificados():
    try:
        # Configuração da conexão com o banco de dados MySQL
        config = {
            'user': 'root',
            'password': 'amarelo123*',
            'host': 'localhost',
            'database': 'horacom'
        }

        # Conectar ao banco de dados
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Consulta para obter os dados dos certificados
        cursor.execute('SELECT email, grupo, opcao, quantidade_horas FROM Certificados')

        # Obter os resultados da consulta
        resultados = cursor.fetchall()

        # Construir o relatório
        relatorio = []
        for resultado in resultados:
            id_aluno, grupo, opcao, quantidade_horas = resultado
            relatorio.append(f'ID Aluno: {id_aluno}, Grupo: {grupo}, Opção: {opcao}, Horas: {quantidade_horas}')

        return relatorio

    except mysql.connector.Error as e:
        print('Erro ao gerar o relatório:', str(e))

    finally:
        # Fechar a conexão
        conn.close()

# Exemplo de uso para gerar o relatório de certificados
relatorio = gerar_relatorio_certificados()
for linha in relatorio:
    print(linha)
