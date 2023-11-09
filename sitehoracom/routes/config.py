import mysql.connector

def get_db_config():
    # Aqui você deve retornar os detalhes de configuração do banco de dados, como um dicionário
    db_config = {
        'user': 'root',
        'password': 'amarelo123*',
        'host': 'localhost',
        'database': 'horacom'
        # outros detalhes de configuração, se aplicável
    }
    return db_config



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

