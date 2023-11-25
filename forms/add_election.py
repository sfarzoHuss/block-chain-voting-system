from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import Length
from wtforms.validators import DataRequired

class AddElectionForm(FlaskForm):
    id = IntegerField('Id Election', validators=[DataRequired()])
    purpose = StringField('Purpose', validators=[DataRequired(), Length(min=1, max=32)])