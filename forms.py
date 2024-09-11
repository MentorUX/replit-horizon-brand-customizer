from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileAllowed
from models import User
import re

def validate_hex_color(form, field):
    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', field.data):
        raise ValidationError('Invalid hex color code')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CustomizationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    logo = FileField('Logo', validators=[FileAllowed(['jpg', 'png', 'gif', 'svg'])])
    brand_color = StringField('Brand Color', validators=[DataRequired(), validate_hex_color])
    button_primary_default_color_bg = StringField('Primary Button Background Color', validators=[DataRequired(), validate_hex_color])
    button_primary_default_color_text = StringField('Primary Button Text Color', validators=[DataRequired(), validate_hex_color])
    button_primary_default_color_stroke = StringField('Primary Button Border Color', validators=[validate_hex_color])
    button_radius = StringField('Button Corner Radius', validators=[DataRequired()])
    button_primary_hover_color_bg = StringField('Primary Button Hover Background Color', validators=[DataRequired(), validate_hex_color])
    button_primary_hover_color_text = StringField('Primary Button Hover Text Color', validators=[DataRequired(), validate_hex_color])
    button_primary_hover_color_stroke = StringField('Primary Button Hover Border Color', validators=[validate_hex_color])
    submit = SubmitField('Save Customization')
