"""
app/extensions.py — extension singletons, initialised in the app factory.
Kept separate to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_mail import Mail
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()
mail = Mail()
csrf = CSRFProtect()
