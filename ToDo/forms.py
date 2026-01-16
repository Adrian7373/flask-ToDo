from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, SubmitField, BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from ToDo.models import User


class FolderForm(FlaskForm):
    name = StringField('Name:',validators=[DataRequired(), Length(min=1,max=100)])
    color = StringField('Color:')
    submit = SubmitField(name="folder-submit")

class TaskForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=1,max=100)])
    description = StringField(validators=[Length(min=1,max=300)])
    is_completed = BooleanField()
    dueDate = DateTimeLocalField('Due Date & Time',format='%Y-%m-%dT%H:%M')
    submit = SubmitField(name="task-submit")

class SubTaskForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=1,max=100)])
    is_completed = BooleanField()
    submit = SubmitField(name="subtask-submit")

class RegisterForm(FlaskForm):

    def validate_username(self, user_to_check):
        user = User.query.filter_by(username=user_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")

    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email address already registered! Please try a different email address")

    username = StringField('Username:', validators=[DataRequired(), Length(min=6,max=20)])
    email = StringField('Email:', validators=[Email(), Length(max=50)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(name="register-submit", label="Register")

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=6,max=20)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(name="login-submit", label="Login")