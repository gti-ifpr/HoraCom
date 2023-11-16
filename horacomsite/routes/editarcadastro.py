from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

# Dados do cadastro (simulação de um cadastro existente)
cadastro = {
    'nome': 'João da Silva',
    'email': 'joao@example.com',
    'cpf': '8945672310',
    'senha': '******'
}

@app.route('/editar_cadastro', methods=['GET', 'POST'])
def editar_cadastro():
    if request.method == 'POST':
        # Atualiza os dados do cadastro com os valores do formulário
        cadastro['nome'] = request.form['name']
        cadastro['email'] = request.form['email']
        cadastro['cpf'] = request.form['cpf']
        cadastro['senha'] = request.form['senha']
        return redirect(url_for('cadastro_atualizado'))

    return render_template('editarcadastro.html', cadastro=cadastro)

@app.route('/cadastro_atualizado')
def cadastro_atualizado():
    return "Cadastro atualizado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
