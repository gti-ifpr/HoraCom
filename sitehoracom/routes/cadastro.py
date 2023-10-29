from flask import request, redirect, url_for, render_template, Blueprint, current_app
import mysql.connector
import config


cadastro_bp = Blueprint("cadastro",__name__)
# Rota para exibir o formulário de cadastro
@cadastro_bp.route('/cadastro', methods=['GET'])
def exibir_formulario_cadastro():#Alterei em 29/10/2023 era def cadastro
    return current_app.send_static_file('index/login/cadastro.html')

# Rota para processar o envio do formulário
@cadastro_bp.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    nome = request.form['nome']
    cpf = request.form['cpf'].replace(".","").replace("-","")
    tipo_usuario = request.form['tipo_usuario']
    email = request.form['email']
    senha = request.form['senha']
    #print (nome)
    
    conexao = mysql.connector.connect(**config.get_db_config())
    try:
        cursor = conexao.cursor()

        consulta = f"INSERT INTO horacom.aluno (nome, cpf, tipo_usuario, email, senha) VALUES ('{nome}', '{cpf}', '{tipo_usuario}', '{email}', '{senha}')"
        #print(consulta)
        cursor.execute(consulta)

        conexao.commit()
    except Exception as e:
        #print (e)
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for('cadastro.exibir_formulario_cadastro'))  # Redireciona de volta para o formulário após a inserção
