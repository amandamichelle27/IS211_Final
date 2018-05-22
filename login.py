# Third-party imports.
from flask_login import LoginManager

# Local imports.
from config import app

# Basic configuration for the login manager to be re-used across components.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"