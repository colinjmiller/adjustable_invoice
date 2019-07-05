from flask import Flask

app = Flask(__name__)

from .views import home
from .views import invoices
app.register_blueprint(home.blueprint, url_prefix='/')
app.register_blueprint(invoices.blueprint, url_prefix='/invoices')


# Configure settings for the environment
app.secret_key = 'CHANGEME'

# Session management
from flask_login import LoginManager
from .svc.users.api import UsersAPI
login_manager = LoginManager()
login_manager.login_view = "home.index"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UsersAPI.get_user_by_id(user_id)

# Hook up the database
from .svc.base import db
from .svc.users.models import User
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql://postgres:password@adjustable_invoice_db/adjustable_invoice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Using a basic assets pipeline, no need for anything fancy
from .util import assets
assets.register_assets(app)

# Add custom jinja2 filters for use in templates
from .util import filters
filters.register_filters(app)

# Any any other helper functions that aren't quite filters
from .util import helpers
app.jinja_env.globals.update(helpers=helpers)
