from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='too')])
    #password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=5, message="长度不符合")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')
