from flask_api import FlaskAPI

# local import
from instance.config import app_config
from svcmgr.blueprints.services import services
from svcmgr.models import db


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(services)

    return app
