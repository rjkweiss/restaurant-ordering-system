from collections import defaultdict
from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..forms.forms import NewOrderForm
from ..models import Employee, MenuItem, Order, OrderDetail, Table, db

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = NewOrderForm()

    form.employee_id.choices = [(0, "Servers")] + [
        (employee.id, employee.name) for employee in Employee.query.all()
    ]
    open_tables_id = [
        order.table_id for order in Order.query.filter_by(finished=False).all()
    ]
    available_tables = Table.query.filter(~Table.id.in_(open_tables_id)).all()
    form.table_id.choices = [(0, "Open Tables")] + [
        (table.id, f"Table {table.number} (Seats {table.capacity})")
        for table in available_tables
    ]

    if form.validate_on_submit():
        # handle the place holders
        if form.employee_id.data == 0 or form.table_id.data == 0:
            flash("Please select a valid server or table", "error")
            return redirect(url_for("dashboard.index"))
        order = Order(
            employee_id=current_user.id, table_id=form.table_id.data, finished=False
        )

        db.session.add(order)
        db.session.commit()
        flash("Table assigned and order created!", "success")
        return redirect(url_for("dashboard.index"))

    open_orders = Order.query.filter_by(
        employee_id=current_user.id, finished=False
    ).all()

    items_by_type = defaultdict(list)
    for item in MenuItem.query.all():
        items_by_type[item.type.name].append(item)

    return render_template(
        "/dashboard/dashboard.html",
        form=form,
        open_orders=open_orders,
        items_by_type=items_by_type,
        title="Server dashboard",
    )


@bp.route("/add-to-order", methods=["POST"])
def add_to_order():
    order_id = request.form.get("order_id")
    menu_items_id = request.form.getlist("menu_items")

    order = Order.query.get_or_404(order_id)

    for item_id in menu_items_id:
        qty = int(request.form.get(f"quantity_{item_id}", 1))
        for _ in range(qty):
            detail = OrderDetail(order=order, menu_item_id=item_id)
            db.session.add(detail)
    db.session.commit()
    flash("Items added to order!", "success")
    return redirect(url_for("dashboard.index"))


@bp.route("/order/<int:order_id>/receipt")
def view_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    table = order.table
    server = order.employee

    items = (
        db.session.query(
            MenuItem.name,
            MenuItem.price,
            db.func.count(OrderDetail.id).label("quantity"),
            (db.func.count(OrderDetail.id) * MenuItem.price).label("subtotal"),
        )
        .join(OrderDetail)
        .filter(OrderDetail.order_id == order.id)
        .group_by(MenuItem.id)
        .all()
    )

    subtotal = sum(item.subtotal for item in items)
    tax_rate = Decimal("0.08875")
    tip_rate = Decimal("0.18")

    sales_tax = round(subtotal * tax_rate, 2)
    gratuity = round(subtotal * tip_rate, 2)
    total = round(subtotal + sales_tax + gratuity, 2)

    return render_template(
        "/dashboard/receipt.html",
        order=order,
        table=table,
        server=server,
        items=items,
        subtotal=subtotal,
        sales_tax=sales_tax,
        gratuity=gratuity,
        total=total,
    )

@bp.route('/order/<int:order_id>/paid', methods=['GET', 'POST'])
def mark_paid(order_id):
    order = Order.query.get_or_404(order_id)
    order.finished = True
    db.session.commit()

    flash(f"Order for Table {order.table.number} marked as paid!", "success")
    return redirect(url_for("dashboard.index"))
