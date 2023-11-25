from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=1, max=50)])
    password = StringField('Password', validators=[DataRequired(), Length(min=1, max=50)])