import os
os.environ['APP_HOME'] = os.path.dirname(__file__)

from .log import get_logger

# Create logger for this module
logger = get_logger(__name__)


from .config import load_settings
load_settings()

from flask import Flask
# from bluprints.api import api_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SERVER_NAME'] = os.environ['SERVER_NAME']
app.config['DEBUG'] = os.environ['ENV'] == 'development'

# app.register_blueprint(api_bp)



# Import the app routes
# from myapp import routes
