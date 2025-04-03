from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import login_required

from app.forms.forms import AddItemsForm, NewOrderForm

from ..models import Employee, MenuItem, Order, OrderDetail, Table, db

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
    available_tables = Table.query.filter(~Table.id.in_(open_table_ids)).all()

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
        return redirect(url_for("orders.view_order", order_id=order.id))

    return render_template("orders/new_order.html", form=form)

@bp.route("/<int:order_id>")
def view_order(order_id):
    order =Order.query.get(order_id)
    if not order:
        abort(404)

    return render_template("orders/order_view.html", order=order)

@bp.route("/<int:order_id>/add_items", methods=['GET', 'POST'])
def add_items(order_id):
    order = Order.query.get_or_404(order_id)
    form = AddItemsForm()

    # populate dropdown with all menu items
    form.menu_items.choices = [(item.id, f"{item.name} (${item.price:.2f})") for item in MenuItem.query.all()]

    if form.validate_on_submit():
        print("form validated on submit")
        for menu_item_id in form.menu_items.data:
            item = OrderDetail(menu_item_id=menu_item_id, order=order)
            db.session.add(item)

        db.session.commit()
        flash("Items successfully added to order!", "success")
        return redirect(url_for("orders.view_order", order_id=order.id))

    return render_template("orders/add_items.html", order=order, form=form)


@bp.route("/<int:order_id>/close", methods=['POST'])
def close_order(order_id):
    order = Order.query.get_or_404(order_id)

    if order.finished:
        flash('Order is already closed. ', "info")
    else:
        order.finished = True
        db.session.commit()
        flash("Order has been closed.", "success")

    return redirect(url_for("orders.view_order", order_id=order.id))
