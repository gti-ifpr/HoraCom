from routes.cadastro import cadastro_bp
from routes.login import login_bp
from flask import Flask, render_template, request, redirect, url_for
from routes.config import get_db_config
import mysql.connector
from routes.cadastro import processar_cadastro

app = Flask(__name__, static_folder='static', static_url_path='') 
app.register_blueprint(cadastro_bp)
app.register_blueprint(login_bp)

def initialize_database():
    global conexao
    conexao = mysql.connector.connect(**get_db_config())


@app.route('/')
def index():
    return render_template('index/index.html')

from flask import request, render_template, redirect, url_for, session

@app.route('/acesso')
def login():
    if 'email' in session:
        # Usuário já está logado
        return redirect(url_for('pagina_de_redirecionamento'))
    return render_template('index/login/login.html')

@app.route('/processar_login', methods=['POST'])
def processar_login():
    email = request.form['email']
    senha = request.form['senha']

    conexao = mysql.connector.connect(**get_db_config())
    cursor = conexao.cursor()

    consulta = f"SELECT tipo_usuario FROM usuarios WHERE email = '{email}' AND senha = '{senha}'"

    cursor.execute(consulta)
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        tipo_usuario = resultado[0]
        session['email'] = email  # Defina o email na sessão
        if tipo_usuario == 'academico':
            return redirect(url_for('pagina_do_academico'))
        elif tipo_usuario == 'coordenador':
            return redirect(url_for('pagina_do_coordenador'))
        else:
            return redirect(url_for('acesso'))

    return redirect(url_for('acesso')) 

# Páginas para usuários de diferentes tipos
@app.route('/pagina_do_academico')
def pagina_do_academico():
    return render_template('index/usuario/useracademic.html')

@app.route('/pagina_do_coordenador')
def pagina_do_coordenador():
    return render_template('index/usuario/usercoordenador.html')


@app.route('/contato')
def contato():
    return render_template('index/contato.html')

@app.route('/sobre')
def sobre():
    return render_template('index/sobre.html')

@app.route('/sobre/storyboard')
def storyboard():
    return render_template('index/sobre/storyboard.html')

@app.route('/sobre/idealizadoras')
def idealizadoras():
    return render_template('index/sobre/idealizadoras.html')

@app.route('/sobre/persona')
def persona():
    return render_template('index/sobre/persona.html')

@app.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    
    email = request.form['email']
    senha = request.form['senha']

    # Exemplo simplificado de conexão com o banco e inserção de dados
    conexao = mysql.connector.connect(**get_db_config())
    cursor = conexao.cursor()

    # Execute a lógica de inserção no banco de dados com os dados fornecidos
    try:
        consulta = f"INSERT INTO tabela_usuarios ( email, senha) VALUES ( '{email}', '{senha}')"
        cursor.execute(consulta)
        conexao.commit()
        cursor.close()
        conexao.close()
        return 'Cadastro processado com sucesso!'
    except Exception as e:
        # Em caso de erro, desfaça a operação e retorne uma mensagem de erro
        conexao.rollback()
        cursor.close()
        conexao.close()
        return 'Erro no processamento do cadastro.'


@app.route('/esqueceusenha')
def esqueceu_senha():
    # Lógica para página de esqueceu a senha
    return render_template('index/login/esqueceusenha.html')

@app.route('/usercoordenador')
def user_coordenador():
    # Lógica para a página do coordenador
    return render_template('index/usuario/usercoordenador.html')

@app.route('/useracademic')
def user_academic():
    # Lógica para a página do coordenador
    return render_template('index/usuario/usercoordenador.html')

@app.route('/login/cadastro')
def cadastro():
    # Lógica para página de cadastro
    return render_template('index/login/cadastro.html')

@app.route('/login/editarcadastro')
def editar_cadastro():
    # Lógica para editar o cadastro
    return render_template('index/login/editarcadastro.html')

@app.route('/relatorio')
def relatorio():
    # Lógica para a página de relatório
    return render_template('relatorio.html')

@app.route('/saibamais')
def saibamais():
    # Lógica para a página de saibamais
    return render_template('saibamais.html')

@app.route('/upload')
def upload():
    # Lógica para a página de upload
    return render_template('upload.html')

@app.route('/editar')
def editar():
    # Lógica para a página de editar
    return render_template('editar.html')

@app.route('/tabela')
def tabela():
    # Lógica para a página de editar
    return render_template('tabela.html')

@app.route('/extrairzip')
def extrair():
    # Lógica para a página de editar
    return render_template('extrairzip.html')



if __name__ == '__main__':
    app.run()
