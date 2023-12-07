from flask import Flask, render_template, request, redirect, url_for, session,redirect,flash,abort,current_app
from flask_login import (
    UserMixin, 
    LoginManager, 
    login_user, 
    login_required, 
    logout_user, 
    current_user
)
from flask_sqlalchemy import SQLAlchemy # Biblioteca para bd
import mysql.connector # para conectar mysql 
from routes.models import User
from flask import jsonify
from flask_mail import Mail, Message
from routes.config import db_get_config, somar_horas_certificados
from sqlalchemy import func, inspect



app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'CamilaFer123*'  
login_manager = LoginManager(app)
login_manager.login_view = 'acesso'
mail = Mail(app)


# Inicialize o objeto SQLAlchemy com a aplicação Flask
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:amarelo123*@localhost/horacom'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


with app.app_context():
    conexao = mysql.connector.connect(**db_get_config())


# Recupera o usuário do banco de dados com base no email - com flask-login
@login_manager.user_loader
def load_user(user_id):    
    usuario = User.query.filter_by(email=user_id).first()
    return usuario

#Rota da pagina incial
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acesso/<data>', methods=['GET'])
def acesso():
    # Verifica se 'email' está na sessão
    if 'email' in session:
        data = request.args.get('data')
        next_url = request.args.get('next')

        # Redireciona com base em 'data' e 'next_url'
        if data:
            return redirect(url_for('user_academic', email=session['email'], data=data, next=next_url) if next_url else url_for('user_academic', email=session['email'], data=data))
        else:
            return redirect(url_for('user_academic', email=session['email'], next=next_url) if next_url else url_for('user_academic', email=session['email']))

    # Se 'email' não estiver na sessão, renderiza o template de login
    return render_template('login.html')

#Acesso para pagina de login
@app.route('/login') 
def login():
    return render_template('login.html')

#Rota que verifica se o usuario ja tem cadastro e direciona(validação com bd)
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
                    return redirect(url_for('user_academic',data=email)) #variavel data = dado email
                elif tipo_usuario == 'coordenador':
                    print("User coordenador")
                    return redirect(url_for('user_coordenador'))
                else:
                    return redirect(url_for('acesso'))
                    
        except mysql.connector.Error as err:
            print(f"Erro na consulta ao banco de dados: {err}")
            return redirect(url_for('acesso'))
        finally:
            # Modificamos esta parte para consumir todos os resultados
            cursor.fetchall()
            cursor.close()

    conexao.close()
    return redirect(url_for('acesso'))

#Rota da Pagina do Academico
@app.route('/user_academic/<data>')#mudar rota com dado do email
def user_academic(data):#variavel data contem email - para vincular o acesso do usuario
    #print("Tipo de usuário:", current_user.tipo_usuario)
    print("Renderizando useracademic.html")
    return render_template('useracademic.html',data=data)
    #else:
    #    print("Redirecionando para acesso")
    #    return redirect(url_for('acesso'))

#Rota para pagina do Coordenador
@app.route('/user_coordenador')
def user_coordenador():
    print("Renderizando user_coordenador.html")
    return render_template('user_coordenador.html')

#Rota para sair - ROTA OK
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Rota do cadastro para inserir no banco de dados as informações do usuario - ROTA OK
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
            consulta = f"INSERT INTO usuarios (nome, cpf, tipo_usuario,email, senha) VALUES ('{nome}', '{cpf}', '{tipo_usuario}','{email}', '{senha}')"
            cursor.execute(consulta)
            conexao.commit()
            
            
        except mysql.connector.Error as err:
            print(f"Erro no processamento do cadastro: {err}")
            conexao.rollback()
        finally:
            cursor.close()
            
    return render_template('login.html')

#Rota para acessar a pagina cadastro - ROTA OK
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

#Rota para pagina que inserimos email e depois recebemos link para mudar senha(AINDA NÃO)
@app.route('/esqueceusenha', methods=['GET', 'POST'])
def esqueceusenha():
    if request.method == 'POST':
        # ... lógica de recuperação de senha ...
        return render_template('email_enviado.html')

    return render_template('esqueceusenha.html')

#Rota com link para alterar senha(AINDA NÃO)
@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')

        # Lógica para atualizar a senha do usuário no banco de dados
        
        return redirect(url_for('acesso'))

    # Renderizar a página de redefinição de senha
    return render_template('redefinir_senha.html', token=token)

#Rota para editar cadastro implementar código para editar cadastro no BD (AINDA NÃO)
@app.route('/editar_cadastro')
def editar_cadastro():
    return render_template('editarcadastro.html')

#Rota da pagina anexar - ROTA OK
@app.route('/anexar/<data>')
def anexar(data):
    return render_template('anexar.html',data=data)

#Rota para anexar certificado - ROTA OK
@app.route('/anexar_certificado/<data>',methods=['POST'])
def anexar_certificado(data):
    # print('entrou')
    anexo = request.form['arquivo']
    # print('anexo ok')
    grupo = request.form['grupoPrincipal']
    # print(grupo)
    
    hora = int(request.form['horasDesejadas'])
    
    if (grupo == 'g1'):
        opcao = request.form['subGrupoG1']
        if opcao == "opcao1":
            hora = hora/4
        elif opcao =="opcao5" or opcao == "opcao9" or opcao == "opcao16":
            hora = hora/2
        elif opcao == "opcao3" or opcao == "opcao11":
            hora = 20
        elif opcao == "opcao4":
            hora = 1
        elif opcao == "opcao10" or opcao == "opcao13":
            hora = 40
        elif opcao == "opcao12":
            hora = 10        
        elif opcao == "opcao14":
            hora = 80
        elif opcao == "opcao17":
            hora = 6        
        elif opcao == "opcao18":
            hora = 3
        # print("entrou g1")
    else:
        # print("entrou g2")
        opcao = request.form['subGrupoG2']
        if opcao == "opcao1" or opcao == "opcao2":
            hora = hora/4
        elif opcao == "opcao3":
            hora = 10
        else:
            if hora > 30:
                hora = 30



    if (grupo == 'g1'):
        opcao = request.form['subGrupoG1']
        if opcao == "opcao1" or opcao =="opcao2" or opcao == "opcao8" or opcao == "opcao9" or opcao == "opcao15" or opcao == "opcao16" or opcao == "opcao17" or opcao == "opcao18" or opcao == "opcao19":
            peso = 60
        elif opcao=="opcao3" or opcao == "opcao6" or opcao == "opcao10" or opcao == "opcao11" or opcao == "opcao12" or opcao == "opcao13" or opcao == "opcao14":
            peso = 80
        elif opcao=="opcao4" or opcao=="opcao5":
            peso = 20
        else:
            peso =  40
        # print("entrou g1")
    else:
        # print("entrou g2")
        opcao = request.form['subGrupoG2']
        if opcao == "opcao1" or opcao == "opcao2":
            peso = 120
        else:
            peso = 60 

    email = data
    if conexao:
        try:
            cursor = conexao.cursor()
            consulta = f"select sum(hora) from certificados where email = '{email}' and grupo = '{grupo}' and opcao = '{opcao}';"
            cursor.execute(consulta)
            resultado = cursor.fetchone()
                        
        except mysql.connector.Error as err:
            print(f"Erro na soma dos certificados: {err}")
            conexao.rollback()
    #Peso = Quantidade maxima
    #Resultado = Quantidade já computada
    #Hora = Quantidade informada
    print(resultado[0])
    if resultado[0] == None:
        resultado = 0
    else:
        resultado = int(resultado[0])
    if(hora > peso-resultado):
        hora = peso-resultado
    # print(horas)
    #print(email)

    if conexao:
        try:
            cursor = conexao.cursor()
            consulta = f"INSERT INTO certificados (email, grupo, opcao,hora, anexo) VALUES ('{email}', '{grupo}', '{opcao}','{int(hora)}', '{anexo}')"
            cursor.execute(consulta)
            conexao.commit()
                        
        except mysql.connector.Error as err:
            print(f"Erro no processamento do cadastro: {err}")
            conexao.rollback()

    return redirect(url_for('relatorio', data=email))


# Rotina Relatórios OK 
@app.route('/relatorio/<data>')
def relatorio(data):
    cursor = conexao.cursor()
    try:
        print("Entrou na função relatorio_certificados")
        consulta = "SELECT * FROM certificados WHERE email=%s"
        cursor.execute(consulta, (data,))
        resultado = cursor.fetchall()
        print(resultado)

        # Calcular a soma das horas
        email = data  # Use o valor 'data' como o email para a função
        somar_horas = somar_horas_certificados(email)
        print(somar_horas)

    except mysql.connector.Error as err:
        print(f"Erro na consulta ao banco de dados: {err}")
        return redirect(url_for('acesso'))
    finally:
        cursor.close()

    return render_template('relatorio.html', data=resultado, somar_horas=somar_horas)

#Rota para retornar os relatórios do BD de todos para o coordenador(VERIFICAR MELHOR FUNÇÃO)
@app.route('/relatorio_todos_usuarios')
@login_required
def relatorio_todos_usuarios():
    # Verifica se o usuário atual é um coordenador
    if current_user.tipo_usuario != 'coordenador':
        abort(403)  # Retorna um erro 403 Forbidden se o usuário não for um coordenador

    try:
        with mysql.connector.connect(**db_get_config()) as conexao:
            cursor = conexao.cursor(dictionary=True)
            consulta = "SELECT * FROM certificados"
            cursor.execute(consulta)
            certificados = cursor.fetchall()

        return render_template('relatoriocoordenador.html', certifiados=certificados)

    except mysql.connector.Error as err:
        print(f"Erro na consulta do relatório de todos os usuários: {err}")
        return render_template('erro.html', error_message=f"Erro na consulta do relatório: {err}")

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
    app.run(debug=True)
