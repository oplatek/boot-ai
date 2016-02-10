from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    """Accepts a nickname."""
    name = StringField('name', validators=[Required()])
    submit = SubmitField('Login')


class AssignForm(Form):
    """Confirm that you want to assigned new game"""
    submit = SubmitField('New Chat!')
