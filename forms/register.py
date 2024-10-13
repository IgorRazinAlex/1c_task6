from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, IntegerField, \
    EmailField
from wtforms.validators import DataRequired, NumberRange


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired(),
                                          NumberRange(min=1,
                                                      message="Invalid age")])
    password = PasswordField("Password", validators=[DataRequired()])
    password_check = PasswordField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Register")
