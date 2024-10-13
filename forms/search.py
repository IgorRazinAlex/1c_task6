from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class MangaSearchForm(FlaskForm):
    name = StringField("Name (required)", validators=[DataRequired()])
    submit = SubmitField("Search meals")
