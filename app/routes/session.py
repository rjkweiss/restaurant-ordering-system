from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from ..forms.forms import LoginForm
from ..models import Employee

bp = Blueprint("session", __name__, url_prefix="/session")

@bp.route("/", methods=['GET', 'POST'])
def login():
    # redirect user to homepage if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("orders.index"))

    # load login form
    form = LoginForm()

    # validate on submit
    if form.validate_on_submit():
        empl_number = form.employee_number.data
        employee = Employee.query.filter(Employee.employee_number == empl_number).first()

        # check that the password provided matches the password in the database
        if not employee or not employee.check_password(form.password.data):
            return redirect(url_for(".login"))

        # login the user
        login_user(employee)

        # once user has been logged in, redirect to homepage
        return redirect(url_for("orders.index"))

    # render the login form
    return render_template("login.html", form=form)

@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('.login'))
