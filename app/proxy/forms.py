from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange


class ProxyForm(FlaskForm):
    host = StringField('Proxy', validators=[DataRequired(), IPAddress()])
    port = IntegerField('Port', validators=[DataRequired(), NumberRange(min=0, max=65535)])
    submit = SubmitField('Add Proxy')
