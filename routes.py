from flask import render_template
import mysql.connector
from app import app  # Importe o objeto app do arquivo app.py
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Configuração da conexão com o banco de dados
config = {
    "host": "localhost",
    "user": "root",
    "password": "Amarelo123*",
    "database": "horacom"
}


# Função para executar a consulta SQL e retornar os resultados
def consultar_banco():
    conexao = mysql.connector.connect(**config)
    try:
        cursor = conexao.cursor()

        consulta = "SELECT * FROM horacom.aluno"
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        return resultados

    finally:
        cursor.close()
        conexao.close()

# Rota para exibir os resultados da consulta na página
@app.route('/dados_do_banco', methods=['GET'])
def dados_do_banco():
    resultados = consultar_banco()
    return render_template('resultados.html', resultados=resultados)


app = Flask(__name__)

# Defina uma chave secreta para proteger as sessões (pode ser qualquer valor secreto)
app.secret_key = 'chave_secreta'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        emailcpf = request.form['emailcpf']
        password = request.form['password']

        # Verifique as credenciais do usuário (por exemplo, em um banco de dados)
        if verificar_credenciais(emailcpf, password):
            # Autenticação bem-sucedida
            session['emailcpf'] = emailcpf  # Inicie uma sessão para o usuário
            return redirect(url_for('pagina_protegida'))

        # Se as credenciais não forem válidas, retorne uma mensagem de erro

    return render_template('login.html')

@app.route('/pagina_protegida')
def pagina_protegida():
    # Verifique se o usuário está autenticado
    if 'emailcpf' in session:
        return 'Você está logado como ' + session['emailcpf']
    else:
        return 'Acesso não autorizado'

def verificar_credenciais(emailcpf, password):
    # Verifique as credenciais em seu banco de dados ou sistema de autenticação
    # Substitua isso por sua própria lógica de autenticação
    return emailcpf == 'usuario' and password == 'senha'

if __name__ == '__main__':
    app.run(debug=True)
