from dotenv import load_dotenv

load_dotenv()

from app import app  # noqa: E402
from app.models import Employee, Menu, MenuItem, MenuItemType, Table, db  # noqa: E402

with app.app_context():
    db.drop_all()
    db.create_all()

    employee = Employee(
        name='Margot',
        employee_number=1234,
        password="password"
    )

    db.session.add(employee)

    # add some food

    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="sides")

    dinner = Menu(name="Dinner")

    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya=MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    db.session.add(dinner)


    # add tables
    tables = [Table(number=i, capacity=2 + (i % 4)) for i in range(1, 11)]
    db.session.add_all(tables)

    db.session.commit()
