from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class DinnerAddForm(FlaskForm):
    name = StringField("Name of meal (required)", validators=[DataRequired()])
    submit = SubmitField("Add meal")