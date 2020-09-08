import os
from flask import Flask

from . import db
from . import controllers
from . import models

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config:
        app.config.from_pyfile('test_config.py')
    else: 
        app.config.from_pyfile('config.py')
        
    db.init_app(app)
    app.register_blueprint(controllers.contact.blueprint)
    app.register_blueprint(controllers.uploader.xml_blueprint)
    return app