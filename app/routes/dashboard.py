from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from ..forms.forms import NewOrderForm
from ..models import Employee, MenuItem, Order, OrderDetail, Table, db

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = NewOrderForm()

    form.employee_id.choices = [(0, "Servers")] + [(employee.id, employee.name) for employee in Employee.query.all()]
    open_tables_id  = [order.table_id for order in Order.query.filter_by(finished=False).all()]
    available_tables = Table.query.filter(~Table.id.in_(open_tables_id)).all()
    form.table_id.choices = [(0, "Open Tables")] + [(table.id, f"Table {table.number} (Seats {table.capacity})") for table in available_tables]

    if form.validate_on_submit():
        # handle the place holders
        if form.employee_id.data == 0 or form.table_id.data == 0:
            flash('Please select a valid server or table', 'error')
            return redirect(url_for("dashboard.index"))
        order = Order(
            employee_id=current_user.id,
            table_id=form.table_id.data,
            finished=False
        )

        db.session.add(order)
        db.session.commit()
        flash('Table assigned and order created!', 'success')
        return redirect(url_for("dashboard.index"))

    open_orders = Order.query.filter_by(employee_id=current_user.id, finished=False).all()

    items_by_type = defaultdict(list)
    for item in MenuItem.query.all():
        items_by_type[item.type.name].append(item)

    return render_template("dashboard.html", form=form, open_orders=open_orders, items_by_type=items_by_type)

@bp.route("/add-to-order", methods=["POST"])
def add_to_order():
    order_id = request.form.get("order_id")
    menu_items_id = request.form.getlist("menu_items")

    order = Order.query.get_or_404(order_id)

    for item_id in menu_items_id:
        detail = OrderDetail(order=order, menu_item_id=item_id)
        db.session.add(detail)
    db.session.commit()
    flash('Items added to order!', 'success')
    return redirect(url_for("dashboard.index"))
