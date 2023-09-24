import mysql.connector
from flask import Flask
from cadastro import cadastro_bp


app = Flask(__name__, static_folder='static',static_url_path='') 
app.register_blueprint(cadastro_bp) #registrador que está no arquivo cadastro.py

"""@app.route('/')
def test_mysql_connection():
    try:
        # Substitua as informações de conexão com o seu banco de dados MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Amarelo123*',
            database='horacom'
        )

        # Se a conexão for bem-sucedida, retornar uma mensagem de sucesso em HTML
        result_html = "<h1>Conexão com o MySQL bem-sucedida!</h1>"
        conn.close()
    except Exception as e:
        # Se ocorrer um erro de conexão, retornar uma mensagem de erro em HTML
        result_html = f"<h1>Erro ao conectar ao MySQL: {str(e)}</h1>"

    return result_html
"""
if __name__ == '__main__':
    app.run()
