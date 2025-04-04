from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired
from wtforms.widgets import CheckboxInput, ListWidget


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    employee_number = StringField('Employee number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class NewOrderForm(FlaskForm):
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    table_id = SelectField('Table', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign')

class AddItemsForm(FlaskForm):
    menu_items = MultiCheckboxField("Menu Items", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Add Items")
