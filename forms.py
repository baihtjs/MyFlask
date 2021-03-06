from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, DateTimeField, FileField, \
    MultipleFileField, TextAreaField
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

class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,50)])
    body = CKEditorField('Body')
    #body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('保存草稿')
    publish = SubmitField('发布')

class SigninForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(1,10)])
    passoword = PasswordField('Password',validators=[DataRequired()])
    submit1 = SubmitField('Signin')

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(1,10)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit2 = SubmitField('Register')

class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')

class EditNoteForm(NewNoteForm):
    submit = SubmitField('Update')

class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')

class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('订阅')


