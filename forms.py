from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, DateTimeField, FileField, \
    MultipleFileField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='password-too-short')])
    #password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=5, message="长度不符合")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')
    date = DateField('Date')
    datetime = DateTimeField('DateTime')
    email = StringField('Email', validators=[DataRequired(), Email(message='error email format ')])

class UploadForm(FlaskForm):
    #photo = FileField('Upload Image')
    photo = FileField('Upload Image', validators=[FileRequired('no files'), FileAllowed(['jpg','png'], 'Images only!')])
    submit = SubmitField()

class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Multi Image', validators=[DataRequired()])
    submit = SubmitField()

