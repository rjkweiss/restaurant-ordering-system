from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from app.forms.forms import NewOrderForm

from ..models import Employee, Order, Table, db

bp = Blueprint("orders", __name__, url_prefix="")

@bp.route("/")
@login_required
def index():
    return render_template("orders.html")

@bp.route('/new_order', methods=['GET', 'POST'])
def new_order():
    form = NewOrderForm()

    # only employees and open tables
    form.employee_id.choices = [(employee.id, employee.name) for employee in Employee.query.all()]

    # find tables that are available / unoccupied
    open_table_ids = [order.table_id for order in Order.query.filter_by(finished=False).all()]
    available_tables = Table.query.filter(~Table.id._in(open_table_ids)).all()

    # only populate form's dropdown with available tables
    form.table_id.choices = [(table.id, f"Table {table.number} (Seats {table.capacity})") for table in available_tables]

    # submit form
    if form.validate_on_submit():
        order = Order(
            employee_id = form.employee_id.data,
            table_id = form.table_id.data,
            finished = False
        )

        db.session.add(order)
        db.session.commit()
        return redirect(url_for("order.view_order", order_id=order.id))

    return render_template("orders/new_order.html", form=form)
