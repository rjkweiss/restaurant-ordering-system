from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

from app import app  # noqa: E402
from app.models import (  # noqa: E402
    Employee,
    Menu,
    MenuItem,
    MenuItemType,
    Order,
    Table,
    db,
)

with app.app_context():
    db.drop_all()
    db.create_all()

    # Employees
    alice = Employee(
        name='Alice Johnson',
        employee_number=101,
        hashed_password=generate_password_hash("alicepass")
    )
    bob = Employee(
        name='Bob Smith',
        employee_number=102,
        hashed_password=generate_password_hash('bobpass')
    )
    clara = Employee(
        name='Clara Lopez',
        employee_number=103,
        hashed_password=generate_password_hash('clarapass')
    )

    db.session.add_all([alice, bob, clara])

    # Tables -- capacity varies from 2 - 5
    tables = [Table(number=i, capacity=2 + (i % 4)) for i in range(1, 11)]
    db.session.add_all(tables)

    # Menu Item Types
    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="sides")
    db.session.add_all([beverages, entrees, sides])

    # Menu and Items
    dinner = Menu(name="Dinner")
    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya=MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)
    db.session.add(dinner)

    # Open order for Table 1
    open_order = Order(employee=alice, table=tables[0], finished=False)
    db.session.add(open_order)

    db.session.commit()
