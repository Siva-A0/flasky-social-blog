from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[DataRequired() , Length(1,64) , Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')
    
class RegistrationForm(FlaskForm):
    email = StringField('Email' , validators=[DataRequired() , Length(1,64) , Email()])
    username = StringField('Username', validators=[DataRequired() , Length(1,64) , Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired() , Length(1,64) , EqualTo('password2',message = 'Passwords must match. ')])
    password2 = PasswordField('Confirm Password' , validators = [DataRequired()] )
    submit = SubmitField('Register')
    
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already Registered. ')
    
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use. ')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("old password",validators=[DataRequired()])
    password = PasswordField('New Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match. ')])
    password2 = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField("Update Password")

class PasswordRequestResetForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Length(1,64),Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    
class EmailChangeForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')
    
    def validate_email(self,field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
