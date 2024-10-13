from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateField
from wtforms.validators import DataRequired


class CheckCPFC(FlaskForm):
    from_date = DateField("Start date of graphic (included) (required)", validators=[DataRequired()])
    to_date = DateField("End date of graphic (included) (required)", validators=[DataRequired()])
    submit = SubmitField("Get graphics")
