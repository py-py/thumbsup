from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ProxyForm(FlaskForm):
    host = StringField('Proxy', validators=[DataRequired(), IPAddress()])
    port = IntegerField('Port', validators=[DataRequired(), NumberRange(min=0, max=65535)])
    submit = SubmitField('Add Proxy')
