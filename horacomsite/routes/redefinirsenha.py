from flask_mail import Mail, Message
from flask import url_for
from routes.email_utils import enviar_email_redefinicao


mail = Mail()


def enviar_email_redefinicao(email, token):
    # Construa o link para redefinir a senha
    link = url_for('redefinir_senha', token=token, _external=True)

    # Construa a mensagem de e-mail
    msg = Message('Redefinição de Senha', sender='horacomgti@gmail.com', recipients=[email])
    msg.body = f'Clique no link para redefinir sua senha: {link}'

    # Envie o e-mail
    mail.send(msg)



