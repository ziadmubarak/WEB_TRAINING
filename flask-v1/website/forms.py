from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField, FloatField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    role = RadioField('Role', choices=[('player','Player'),('coach','Coach')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class PlayerInputForm(FlaskForm):
    position = SelectField('Position', choices=[('point_guard', 'Point Guard'), ('shooting_guard', 'Shooting Guard'), ('small_forward', 'Small Forward'), ('power_forward', 'Power Forward'), ('center', 'Center')])
    height = FloatField('Height (in cm)', validators=[DataRequired()])
    weight = FloatField('Weight (in kg)', validators=[DataRequired()])
    finishing = IntegerField('Finishing (out of 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    shooting = IntegerField('Shooting (out of 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    handles = IntegerField('Handles (out of 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    rebounding = IntegerField('Rebounding (out of 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    defense = IntegerField('Defense (out of 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Submit')



