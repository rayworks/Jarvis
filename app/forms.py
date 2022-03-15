from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField('Username', [
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', [Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
