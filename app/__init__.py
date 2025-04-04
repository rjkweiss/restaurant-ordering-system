import os

from flask import Flask
from flask_login import LoginManager

from .config import Config
from .models import Employee, db
from .routes import dashboard, orders, public, session

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder=os.path.join(basedir, "..", "static"))
app.config.from_object(Config)
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(public.bp)

# configure the application with SQLAlchemy
db.init_app(app)

# configure Flask Login
login = LoginManager(app)
login.login_view = "session.login"

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))
