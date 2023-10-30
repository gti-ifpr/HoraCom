from routes.cadastro import cadastro_bp
from routes.login import login_bp
from flask import Flask, render_template, request, redirect, url_for
from routes.config import get_db_config
import mysql.connector

conexao = mysql.connector.connect(**get_db_config())

app = Flask(__name__, static_folder='static', static_url_path='') 
app.register_blueprint(cadastro_bp)
app.register_blueprint(login_bp)

@app.route('/')
def index():
    return render_template('index/index.html')

@app.route('/acesso')
def login():
    return render_template('index/login/login.html')

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
    # Lógica para processar o cadastro
def processar_cadastro():
    return 'Cadastro processado com sucesso!'

@app.route('/esqueceusenha')
def esqueceu_senha():
    # Lógica para página de esqueceu a senha
    return render_template('index/login/esqueceusenha.html')

@app.route('/usercoordenador')
def user_coordenador():
    # Lógica para a página do coordenador
    return render_template('index/login/usercoordenador.html')

@app.route('/useracademic')
def user_academic():
    # Lógica para a página do coordenador
    return render_template('index/aluno/usercoordenador.html')

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
