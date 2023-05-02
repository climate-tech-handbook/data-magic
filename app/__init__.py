from flask import Flask
from app.api import api_bp

app = Flask(__name__)

from app.api import routes

app.register_blueprint(api_bp)