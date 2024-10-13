from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FileField
from wtforms.validators import DataRequired


class MealAddForm(FlaskForm):
    name = StringField("Name (required)", validators=[DataRequired()])
    calories = StringField("Calories per 100 gramm (required)", validators=[DataRequired()])
    proteins = StringField("Proteins per 100 gramm (required)", validators=[DataRequired()])
    fats = StringField("Fats per 100 gramm (required)", validators=[DataRequired()])
    carbonades = StringField("Carbonades per 100 gramm (required)", validators=[DataRequired()])
    about = TextAreaField("About (non optional)")
    preview = FileField("Preview (required)", validators=[DataRequired()])
    submit = SubmitField("Add meal")
