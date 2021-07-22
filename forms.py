from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Optional, Length, NumberRange, URL



class UserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=20)])
    password = StringField('Password', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])