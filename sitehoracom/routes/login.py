from flask import request, redirect, url_for, render_template, Blueprint, current_app, session
import mysql.connector
import config


login_bp = Blueprint("login", __name__)

# Rota para exibir o formulário de login
@login_bp.route('/login', methods=['GET'])
def login():
    return current_app.send_static_file('login.html')

# Rota para processar o envio do formulário de login
@login_bp.route('/processar_login', methods=['POST'])
def processar_login():
    email = request.form['email']
    senha = request.form['senha']

    conexao = mysql.connector.connect(**config.get_db_config())

    try:
        cursor = conexao.cursor()
        consulta = f"SELECT * FROM horacom.aluno WHERE email = '{email}' AND senha = '{senha}'"
        cursor.execute(consulta)
        #print(consulta)
        resultado = cursor.fetchone()

        if resultado:
            # Defina uma variável de sessão para rastrear o usuário logado
            session['user_id'] = resultado[0]
            # Redirecione para a página de perfil do usuário ou outra página após o login
            return redirect(url_for('perfil'))  # Substitua 'perfil' pelo nome da sua rota de perfil
    
    except Exception as e:
        # print(e)
        conexao.rollback()


    finally:
        cursor.close()
        conexao.close()

    # Redireciona de volta para a página de login em caso de falha de autenticação
    return redirect(url_for('.login'))

# Rota de logout
@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove a variável de sessão para encerrar a sessão do usuário
    return redirect(url_for('.login'))