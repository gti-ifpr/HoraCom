import sqlite3

# Função para inserir um certificado na tabela Certificados
def inserir_certificado(id_aluno, grupo, opcao, quantidade_horas):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('horacom.db')
    cursor = conn.cursor()

    try:
        # Inserir os dados na tabela Certificados
        cursor.execute("INSERT INTO Certificados (id_aluno, grupo, opcao, quantidade_horas) VALUES (?, ?, ?, ?)",
                       (id_aluno, grupo, opcao, quantidade_horas))

        # Commit para salvar as alterações
        conn.commit()
        print("Certificado inserido com sucesso!")
    except sqlite3.Error as e:
        print("Erro ao inserir certificado:", str(e))
    finally:
        # Fechar a conexão com o banco de dados
        conn.close()

# Exemplo de uso da função
inserir_certificado(1, 'g1', 'Opção 1', 30.5)

