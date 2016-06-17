from flask import Flask
app = Flask(__name__)

from . import entry #make decorators work

@app.before_first_request
def application_initialize():
    pass