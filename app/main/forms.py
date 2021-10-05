from flask_wtf import Form
from wtforms.fields import StringField, SubmitField,PasswordField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Your Email', validators=[Required()])
    password = PasswordField('Your Password', validators=[Required()])
    room = StringField('Meeting Name/Id', validators=[Required()],default='DotsChat')
    submit = SubmitField('Login now')
class RegisterForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Your Name', validators=[Required()])
    email = StringField('Your Email', validators=[Required()])
    password = PasswordField('Your Password', validators=[Required()])
    #room = StringField('Meeting Name/Id', validators=[Required()],default='DotsChat')
    submit = SubmitField('Register now')