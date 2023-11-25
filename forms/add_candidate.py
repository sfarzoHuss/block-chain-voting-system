from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import Length
from wtforms.validators import DataRequired

class AddCandidateForm(FlaskForm):
    id = IntegerField('Id Candidate', validators=[DataRequired()])
    name = StringField('Name Candidate', validators=[DataRequired(), Length(min=1, max=32)])
    lastname = StringField('Lastname Candidate', validators=[DataRequired(), Length(min=1, max=32)])
    manifesto = StringField('Manifesto', validators=[DataRequired(), Length(min=1, max=32)])