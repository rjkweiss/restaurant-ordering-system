# from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.Integer, nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    # relationships
    orders = db.relationship("Order", back_populates="employee")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Menu(db.Model):
    __tablename__ = 'menus'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    # one-to-many relationship with menu items
    items = db.relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan")

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    menu_type_id = db.Column(db.Integer, db.ForeignKey("menu_item_types.id"), nullable=False)

    # relationships
    menu = db.relationship("Menu", back_populates="items")
    type = db.relationship("MenuItemType", back_populates="items")

class MenuItemType(db.Model):
    __tablename__ = 'menu_item_types'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    # one-to-many relationship to Menu Item
    items = db.relationship("MenuItem",  back_populates="type", cascade="all, delete-orphan")

class Table(db.Model):
    __tablename__ = 'tables'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)

    # relationship
    orders = db.relationship('Order', back_populates='table')

class Order(db.Model):
    __tablename__ = 'orders'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # relationships
    employee = db.relationship("Employee", back_populates="orders")
    table = db.relationship('Table', back_populates='orders')
    details = db.relationship('OrderDetail', back_populates='order', cascade="all, delete-orphan")

class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)

    # relationship
    order = db.relationship('Order', back_populates='details')
    menu_item = db.relationship('MenuItem')
