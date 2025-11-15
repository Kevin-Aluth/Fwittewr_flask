from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={'placeholder':'Username', 'class':'form-control'})
    password = PasswordField(validators=[DataRequired()], render_kw={'placeholder':'Password', 'class':'form-control'})
    submit = SubmitField('Login', render_kw={'class':'btn btn-primary mt-1 w-100'})

class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username', 'class':'form-control'})
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Password', 'class':'form-control'})
    submit = SubmitField('Register', render_kw={'class':'btn btn-primary mt-1 w-100'})
    def validate_username(self, username):
        existing_username_user = User.query.filter_by(username=username.data).first()
        if existing_username_user:
            raise ValidationError('this username already exists')

class CreatePostForm(FlaskForm):
    title = StringField(validators=[Length(min=0, max=50)], render_kw={'placeholder':'Title', 'class':'form-control'})
    content = TextAreaField(validators=[DataRequired(), Length(min=4, max=200)], render_kw={'placeholder':'Content', 'class':'form-control'})
    submit = SubmitField('Post', render_kw={'class':'btn btn-primary mt-1 w-100'})
