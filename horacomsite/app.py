from flask import (
    Flask, render_template, request, redirect, url_for, session, flash, jsonify,current_app
)
from flask_login import (
    UserMixin, LoginManager,login_user, login_required, logout_user, current_user
)
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import os
import mysql.connector
from routes.config import (
    db, get_db_config, SQLALCHEMY_DATABASE_URI
)
from routes.cadastro import cadastro_bp
from routes.login import login_bp
from routes import *
from routes.redefinirsenha import enviar_email_redefinicao


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


@app.route('/')#Rota da pagina incial
def index():
    return render_template('index.html')


@app.route('/acesso', methods=['GET'])
def acesso():
    if 'email' in session:
        print("Usuário já está logado")
        next_url = request.args.get('next')
        if next_url:
            return redirect(url_for('user_academic') + f'?next={next_url}')
        return redirect(url_for('user_academic'))
    return render_template('login.html')


@app.route('/login')#Login aqui acho que esta duplicado e podemos tentar melhorar 
def login():
    # lógica de login aqui
    return render_template('login.html')

#Rota que verifica se o usuario ja tem cadastro e direciona
@app.route('/processar_login', methods=['POST'])
def processar_login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not email or not senha:
        return redirect(url_for('acesso'))

    app.logger.debug(f"Email: {email}, Senha: {senha}")

    if email and senha:
        cursor = conexao.cursor()
        try:
            consulta = f"SELECT tipo_usuario FROM usuarios WHERE email = '{email}' AND senha = '{senha}'"
            cursor.execute(consulta)
            resultado = cursor.fetchone()

            if resultado:
                tipo_usuario = resultado[0]
                session['tipo_usuario'] = tipo_usuario
                session['email'] = email

                if tipo_usuario == 'academico':
                    print("User academic")
                    return redirect(url_for('user_academic'))
                elif tipo_usuario == 'coordenador':
                    return redirect(url_for('user_coordenador'))
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

#Rota da Pagina do Academico
@app.route('/user_academic')
def user_academic():
    #print("Tipo de usuário:", current_user.tipo_usuario)

    print("Renderizando useracademic.html")
    return render_template('useracademic.html')
    #else:
    #    print("Redirecionando para acesso")
    #    return redirect(url_for('acesso'))

#Rota para pagina do Coordenador
@app.route('/user_coordenador')
def user_coordenador():

    print("Renderizando user_coordenador.html")
    return render_template('user_coordenador.html')

#Rota para sair 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['POST'])
def processar_cadastro():
    email = request.form['email']
    senha = request.form['senha']
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    tipo_usuario = request.form.get('tipo_usuario', 'academico')  # Padrão para 'academico' se não estiver presente
    
    if conexao:
        try:
            cursor = conexao.cursor()
            # Inclua 'nome', 'cpf' e 'tipo_usuario' na consulta SQL
            consulta = f"INSERT INTO usuarios (nome, cpf, tipo_usuario,email, senha) VALUES ('{nome}', '{cpf}', '{tipo_usuario}','{email}', '{senha}')"
            cursor.execute(consulta)
            conexao.commit()
            
            # Restante do código...
            
        except mysql.connector.Error as err:
            print(f"Erro no processamento do cadastro: {err}")
            conexao.rollback()
        finally:
            cursor.close()
            conexao.close()
    return render_template('login.html')

#Rota para pagina que inserimos email e depois recebomos link para mudar senha
@app.route('/esqueceusenha', methods=['GET', 'POST'])
def esqueceusenha():
    if request.method == 'POST':
        # ... lógica de recuperação de senha ...
        return render_template('email_enviado.html')

    return render_template('esqueceusenha.html')

#Rota com link para alterar senha
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

#Rota para editar cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
#Rota com logica para obter dados do BD
@app.route('/obter_registros', methods=['GET'])
def obter_registros():
    if not current_user.is_authenticated:
        return jsonify({"error": "Usuário não autenticado"}), 401

    tipo_usuario = current_user.tipo_usuario

    
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

#Rota para editar cadastro
@app.route('/editar_cadastro')
def editar_cadastro():
    return render_template('editarcadastro.html')


@app.route('/anexar_certificado',methods=['POST'])
def anexar_certificado():
    # print('entrou')
    anexo = request.form['arquivo']
    # print('anexo ok')
    grupo = request.form['grupoPrincipal']
    # print(grupo)
    if (grupo == 'g1'):
        opcao = request.form['subGrupoG1']
        # print("entrou g1")
    else:
        # print("entrou g2")
        opcao = request.form['subGrupoG2']
    # print("retorna")
    horas = request.form['horasDesejadas']
    # print(horas)
    email = request.form['email']
    #print(email)

    if conexao:
        try:
            cursor = conexao.cursor()
            consulta = f"INSERT INTO certificados (email, grupo, opcao,hora, anexo) VALUES ('{email}', '{grupo}', '{opcao}','{horas}', '{anexo}')"
            cursor.execute(consulta)
            conexao.commit()
                        
        except mysql.connector.Error as err:
            print(f"Erro no processamento do cadastro: {err}")
            conexao.rollback()

    return render_template('relatorio.html')

@app.route('/anexar')
def anexar():
    return render_template('anexar.html')

#Rota para os relatório
@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')


@app.route('/relatorio_certificados')
def relatorio_certificados():
    try:
        with mysql.connector.connect(**get_db_config()) as conexao:
            cursor = conexao.cursor(dictionary=True)  # Retorna os resultados como dicionários
            consulta = "SELECT * FROM certificados"
            cursor.execute(consulta)
            certificados = cursor.fetchall()

        return render_template('relatorio.html', resultados=certificados)

    except mysql.connector.Error as err:
        print(f"Erro na consulta do relatório: {err}")
        return render_template('erro.html')

@app.route('/obter_registros_certificados', methods=['GET'])
@login_required
def obter_registros_certificados():
    if not current_user.is_authenticated:
        return jsonify({"error": "Usuário não autenticado"}), 401

    try:
        cursor = conexao.cursor(dictionary=True)
        consulta = f"SELECT email, grupo, opcao, hora, anexo FROM certificados WHERE tipo_usuario = '{current_user.tipo_usuario}'"
        cursor.execute(consulta)
        registros = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro na consulta ao banco de dados: {err}")
        return jsonify({"error": "Erro na consulta ao banco de dados"}), 500
    finally:
        cursor.close()

    # Renderiza o template e passa os registros como variável
    return render_template('relatorio.html', registros=registros)



#Rota para extrair zip
@app.route('/extrairzip')
def extrairzip():
    return render_template('extrairzip.html')

#Rota para upload (Uso do coordenador)
@app.route('/upload')
def upload():
    return render_template('upload.html')



#------------- ROTAS ESTATICAS -----------------#

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/storyboard')
def storyboard():
    return render_template('storyboard.html')

@app.route('/idealizadoras')
def idealizadoras():
    return render_template('idealizadoras.html')

@app.route('/persona')
def persona():
    return render_template('persona.html')    

@app.route('/saibamais')
def saibamais():
    return render_template('saibamais.html')

@app.route('/tabela')
def tabela():
    return render_template('tabela.html')






if __name__ == '__main__':
    app.run()
