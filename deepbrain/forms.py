from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from deepbrain.models import User

class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(),Length(min=2, max=40)])
	email = StringField("Email",validators=[DataRequired(), Email()])
	password = PasswordField("Password",validators=[DataRequired(),Length(min=8)])
	confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username already taken. Please choose different one! ")

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already taken. Please choose different one! ")



class LoginForm(FlaskForm):
	email = StringField("Email",validators=[DataRequired(), Email()])
	password = PasswordField("Password",validators=[DataRequired(),Length(min=8)])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(),Length(min=2, max=40)])
	email = StringField("Email",validators=[DataRequired(), Email()])
	picture = FileField('Update profile picture',validators=[FileAllowed(["jpg","jpeg","png"])])
	submit = SubmitField("Update")

	def validate_username(self,username):
		if current_user.username != username.data:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("Username already taken. Please choose different one! ")

	def validate_email(self,email):
		if current_user.email != email.data:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("Email already taken. Please choose different one! ")

