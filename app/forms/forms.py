from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    employee_number = StringField('Employee number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NewOrderForm(FlaskForm):
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    table_id = SelectField('Table', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Order')
