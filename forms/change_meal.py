from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FileField
from wtforms.validators import DataRequired


class ChangeMealForm(FlaskForm):
    name = StringField("Name")
    calories = StringField("Calories per 100 gramm")
    proteins = StringField("Proteins per 100 gramm")
    fats = StringField("Fats per 100 gramm")
    carbonades = StringField("Carbonades per 100 gramm")
    about = TextAreaField("About")
    preview = FileField("New preview (required)", validators=[DataRequired()])
    submit = SubmitField("Change meal")
