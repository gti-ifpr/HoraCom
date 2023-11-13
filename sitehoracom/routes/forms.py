from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistroForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    tipo_usuario = SelectField('Tipo de Usuário', choices=[('academico', 'Acadêmico'), ('coordenador', 'Coordenador')], validators=[DataRequired()])
    submit = SubmitField('Registrar')
