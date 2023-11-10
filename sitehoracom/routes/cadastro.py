from flask import request, redirect, url_for, render_template, Blueprint, current_app
import mysql.connector
from routes.config import get_db_config


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

    conexao = mysql.connector.connect(**get_db_config())
    cursor = conexao.cursor()

    try:
        consulta = f"INSERT INTO horacom.aluno (nome, cpf, tipo_usuario, email, senha) VALUES ('{nome}', '{cpf}', '{tipo_usuario}', '{email}', '{senha}')"
        cursor.execute(consulta)
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        cursor.close()
        conexao.close()
        return redirect(url_for('login'))  # Em caso de erro na inserção, redirecione para a página de login

    conexao_nova = mysql.connector.connect(**get_db_config())  # Estabelece uma nova conexão
    cursor_novo = conexao_nova.cursor(dictionary=True)  # Novo cursor em modo dicionário

    consulta_verificacao = f"SELECT tipo_usuario FROM horacom.aluno WHERE email = '{email}'"
    cursor_novo.execute(consulta_verificacao)
    usuario_existente = cursor_novo.fetchone()

    cursor_novo.close()  # Fecha o novo cursor
    conexao_nova.close()  # Fecha a nova conexão

    if usuario_existente:
        tipo_usuario = usuario_existente['tipo_usuario']  # Tipo de usuário estará no campo 'tipo_usuario'
        
        if tipo_usuario == '02':
            return render_template('index/usuario/usercoordenador.html')
        elif tipo_usuario == '01':
            return render_template('index/usuario/useracademic.html')

    return redirect(url_for('login'))  # Redireciona para a página de login se não encontrar um usuário ou um tipo desconhecido
