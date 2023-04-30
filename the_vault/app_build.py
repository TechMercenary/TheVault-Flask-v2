from flask import Flask
from bluprints.api import api_bp
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SERVER_NAME'] = os.environ['SERVER_NAME'] 
app.config['DEBUG'] = os.environ['ENV'] == 'development'

app.register_blueprint(api_bp)