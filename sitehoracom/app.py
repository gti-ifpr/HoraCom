from routes.cadastro import cadastro_bp
from routes.login import login_bp
from flask import Flask, render_template, request, redirect, url_for, session,redirect,flash
import mysql.connector
from flask_login import LoginManager
from routes.config import db
from flask_login import (
    UserMixin, 
    LoginManager, 
    login_user, 
    login_required, 
    logout_user, 
    current_user
)
from routes.models import User, Academico, Coordenador
from flask import jsonify
from routes.config import db
from flask_mail import Mail, Message
from routes.redefinirsenha import enviar_email_redefinicao
from routes.config import get_db_config, SQLALCHEMY_DATABASE_URI
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import mysql.connector
from routes.config import get_db_config
from flask_mysqldb import MySQL


app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'CamilaFer123*'  
login_manager = LoginManager(app)
login_manager.login_view = 'acesso'
mail = Mail(app)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT', 587)
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'horacomgti@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'CamilaFer123*')

# Configuração do banco de dados MySQL local
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:amarelo123*@localhost/horacom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialize o objeto SQLAlchemy com a aplicação Flask
db = SQLAlchemy(app)

with app.app_context():
    conexao = mysql.connector.connect(**get_db_config())


@login_manager.user_loader
def load_user(user_id):
    # Implemente a lógica para retornar uma instância do usuário com base no ID do usuário
    # Exemplo hipotético:
    # return Usuario.query.get(int(user_id))
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/acesso')
def acesso():
    if 'email' in session:
        # Usuário já está logado
        return redirect(url_for('acesso'))
    return render_template('login.html')


from flask_login import login_user, logout_user

# ...

@login_manager.user_loader
def load_user(user_id):
    # Implemente a lógica para retornar uma instância do usuário com base no ID do usuário
    # Exemplo hipotético:
    # return Usuario.query.get(int(user_id))
    return None

# ...

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not email or not senha:
        return redirect(url_for('acesso'))

    app.logger.debug(f"Email: {email}, Senha: {senha}")

    if email and senha:
        cursor = conexao.cursor()
        try:
            # Utilizando instrução preparada
            consulta = "SELECT tipo_usuario FROM usuarios WHERE email = %s AND senha = %s"
            cursor.execute(consulta, (email, senha))
            resultado = cursor.fetchone()

            if resultado:
                tipo_usuario = resultado[0]
                
                # Utilizando Flask-Login para gerenciar o login do usuário
                user = User(email)  # Substitua isso com a lógica real para carregar o usuário
                login_user(user)

                if tipo_usuario == 'academico':
                    return redirect(url_for('useracademic'))
                elif tipo_usuario == 'coordenador':
                    return redirect(url_for('usercoordenador'))
                else:
                    return redirect(url_for('acesso'))
                    
        except mysql.connector.Error as err:
            print(f"Erro na consulta ao banco de dados: {err}")
            return redirect(url_for('acesso'))
        finally:
            cursor.fetchall()
            cursor.close()

    conexao.close()
    return redirect(url_for('acesso'))




@app.route('/useracademic')
@login_required
def user_academic():
    print("Tipo de usuário:", current_user.tipo_usuario)

    if current_user.tipo_usuario == 'academico':
        print("Renderizando useracademic.html")
        return render_template('useracademic.html')
    else:
        print("Redirecionando para acesso")
        return redirect(url_for('acesso'))



@app.route('/usercoordenador')
@login_required
def user_coordenador():
    if current_user.tipo_usuario == 'coordenador':
        return render_template('usercoordenador.html')
    else:
        return redirect(url_for('acesso'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('acesso'))

@app.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    try:
        email = request.form['email']
        senha = request.form['senha']
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        tipo_usuario = request.form.get('tipo_usuario', 'academico')  # Padrão para 'academico' se não estiver presente

        conexao = mysql.connector.connect(**get_db_config())

        if conexao:
            with conexao.cursor() as cursor:
                # Utilizando instrução preparada para evitar injeção de SQL
                consulta = "INSERT INTO usuarios (nome, cpf, tipo_usuario, email, senha) VALUES (%s, %s, %s, %s, %s)"
                valores = (nome, cpf, tipo_usuario, email, senha)
                cursor.execute(consulta, valores)

            conexao.commit()
    except mysql.connector.Error as err:
        print(f"Erro no processamento do cadastro: {err}")
        conexao.rollback()
        return 'Erro no processamento do cadastro. Tente novamente.'
    finally:
        conexao.close()

    return 'Cadastro realizado com sucesso!'


@app.route('/esqueceusenha', methods=['GET', 'POST'])
def esqueceusenha():
    if request.method == 'POST':
        # ... lógica de recuperação de senha ...
        return render_template('email_enviado.html')

    return render_template('esqueceusenha.html')

@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    # Lógica para verificar se o token é válido (por exemplo, tem um prazo de validade)
    # e se é associado a um usuário no banco de dados

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')

        # Lógica para atualizar a senha do usuário no banco de dados
        # (Você precisa implementar esta lógica)

        # Redirecionar para a página de login ou outra página apropriada após a redefinição de senha
        return redirect(url_for('acesso'))

    # Renderizar a página de redefinição de senha
    return render_template('redefinir_senha.html', token=token)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/obter_registros', methods=['GET'])
def obter_registros():
    if not current_user.is_authenticated:
        return jsonify({"error": "Usuário não autenticado"}), 401

    tipo_usuario = current_user.tipo_usuario

    # Lógica para obter registros do banco de dados com base no tipo de usuário
    try:
        cursor = conexao.cursor(dictionary=True)
        consulta = f"SELECT * FROM tipos_usuario WHERE tipo = '{tipo_usuario}'"
        cursor.execute(consulta)
        registros = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro na consulta ao banco de dados: {err}")
        return jsonify({"error": "Erro na consulta ao banco de dados"}), 500
    finally:
        cursor.close()

    return jsonify({"registros": registros})

@app.route('/editarcadastro')
def editar_cadastro():
    return render_template('editarcadastro.html')

@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/editar')
def editar():
    return render_template('editar.html')

@app.route('/tabela')
def tabela():
    return render_template('tabela.html')

@app.route('/extrairzip')
def extrair():
    return render_template('extrairzip.html')

#-------------------ROTAS ESTÁTICAS--------------------
@app.route('/saibamais')
def saibamais():
    return render_template('saibamais.html')
@app.route('/idealizadoras')
def idealizadoras():
    return render_template('idealizadoras.html')
@app.route('/persona')
def persona():
    return render_template('persona.html')
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')
@app.route('/storyboard')
def storyboard():
    return render_template('storyboard.html')
@app.route('/contato')
def contato():
    return render_template('contato.html')





if __name__ == '__main__':
    app.run()