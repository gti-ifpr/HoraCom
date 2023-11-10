from flask import request, redirect, url_for, render_template, Blueprint, current_app
import mysql.connector
from routes.config import get_db_config  # Importe a função get_db_config do módulo routes.config

cadastro_bp = Blueprint("cadastro", __name__)

@cadastro_bp.route('/cadastro', methods=['GET'])
def exibir_formulario_cadastro():
    return current_app.send_static_file('index/login/cadastro.html')

@cadastro_bp.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    nome = request.form['nome']
    cpf = request.form['cpf'].replace(".", "").replace("-", "")
    tipo_usuario = request.form['tipo_usuario']
    email = request.form['email']
    senha = request.form['senha']

    conexao = mysql.connector.connect(**get_db_config())  # Use a função importada para obter os detalhes de conexão do banco de dados
    try:
        cursor = conexao.cursor()

        consulta = f"INSERT INTO horacom.aluno (nome, cpf, tipo_usuario, email, senha) VALUES ('{nome}', '{cpf}', '{tipo_usuario}', '{email}', '{senha}')"
        cursor.execute(consulta)

        conexao.commit()
    except Exception as e:
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for('login'))  # Redireciona para a rota 'login' após a inserção
