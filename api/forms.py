from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField,MultipleFileField
from wtforms.validators import DataRequired,Email

class registrationForm(FlaskForm):
	username=StringField("Username",validators=[DataRequired()])
	email=StringField("email",validators=[Email()])
	password=PasswordField("password",validators=[DataRequired()])
	submit=SubmitField("register")

class loginForm(FlaskForm):
	username=StringField("Username",validators=[DataRequired()])
	password=PasswordField("password",validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit=SubmitField("login")

class postForm(FlaskForm):
	story=TextAreaField("story",validators=[DataRequired()])
	picture= MultipleFileField("picture",validators=[FileAllowed(['jpg', 'png'])])
	submit=SubmitField("post")

class editForm(FlaskForm):
	story=TextAreaField("story",validators=[DataRequired()])
	submit=SubmitField("post")