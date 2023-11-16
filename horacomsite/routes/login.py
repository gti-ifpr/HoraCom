from flask import request, redirect, url_for, render_template, Blueprint, current_app, session, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from .models import User  # Suponhamos que você tenha uma classe de modelo User

login_bp = Blueprint("login", __name__)

@login_bp.route('/login', methods=['GET'])
def login():
    return current_app.send_static_file('login.html')

@login_bp.route('/processar_login', methods=['POST'])
def processar_login():
    email = request.form['email']
    senha_digitada = request.form['senha']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.senha_hash, senha_digitada):
        login_user(user)
        flash('Login bem-sucedido!', 'success')
        return redirect(url_for('perfil'))  # Substitua 'perfil' pelo nome da sua rota de perfil
    else:
        flash('Credenciais inválidas. Tente novamente.', 'danger')
        return redirect(url_for('.login'))

@login_bp.route('/logout')
def logout():
    logout_user()
    flash('Logout bem-sucedido!', 'success')
    return redirect(url_for('.login'))
