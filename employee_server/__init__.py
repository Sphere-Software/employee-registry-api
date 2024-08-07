from flask import Flask

from .api import setup_api


app = Flask(__name__)
setup_api(app)
