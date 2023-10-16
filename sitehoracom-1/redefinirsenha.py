from flask import Flask
import mysql.connector

app = Flask(__name__)
#TESTE LOCAL EM PYTHON DEU CERTO
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

def redefinir_senha(usuario, nova_senha):
    try:
        # Atualizar a senha do usuário no banco de dados
        cursor.execute('''
            UPDATE Senhas
            SET senha = %s
            WHERE usuario = %s
        ''', (nova_senha, usuario))

        conn.commit()
        print('Senha redefinida com sucesso para o usuário:', usuario)
    except mysql.connector.Error as e:
        print('Erro ao redefinir a senha:', str(e))

# Exemplo de uso para redefinir a senha para o usuário 'alice'
redefinir_senha('alice', 'nova_senha_para_alice')

# Não se esqueça de fechar a conexão após usar
conn.close()

