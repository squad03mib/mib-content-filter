
#!/usr/bin/env python3

import connexion

from swagger_server import encoder
import os
import connexion
from flask_environments import Environments
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
import json

__version__ = '0.1'

db = None
migrate = None
debug_toolbar = None
redis_client = None
app = None
api_app = None
logger = None


def create_app():
    """
    This method create the Flask application.
    :return: Flask App Object
    """
    global db
    global app
    global migrate
    global api_app

    # first initialize the logger
    init_logger()

    api_app = connexion.FlaskApp(
        __name__,
        server='flask',
        specification_dir='swagger/',
    )

    # getting the flask app
    app = api_app.app

    flask_env = os.getenv('FLASK_ENV', 'None')
    if flask_env == 'development':
        config_object = 'config.DevConfig'
    elif flask_env == 'testing':
        config_object = 'config.TestConfig'
    elif flask_env == 'production':
        config_object = 'config.ProdConfig'
    else:
        raise RuntimeError(
            "%s is not recognized as valid app environment. You have to setup the environment!" % flask_env)

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    # registering db
    db = SQLAlchemy(
        app=app
    )

    # requiring the list of models
    import swagger_server.models_db
    from swagger_server.models_db import ContentFilter

    # checking the environment
    if flask_env == 'testing':
        # we need to populate the db
        db.create_all()

    # registering to api app all specifications
    register_specifications(api_app)

    with app.app_context():
        q = db.session.query(ContentFilter).filter(ContentFilter.name == 'Default')
        content_filter = q.first()
        if content_filter is None:
            default_content_filter = ContentFilter()
            default_content_filter.name = 'Default'
            default_content_filter.id = 1
            default_content_filter.private = False
            word_list = []
            word_list.append("ciao")
            default_content_filter.words = json.dumps(word_list)
            db.session.add(default_content_filter)
            db.session.commit()


    return app


def init_logger():
    global logger
    """
    Initialize the internal application logger.
    :return: None
    """
    logger = logging.getLogger(__name__)
    from flask.logging import default_handler
    logger.addHandler(default_handler)


def register_specifications(_api_app):
    """
    This function registers all resources in the flask application
    :param _api_app: Flask Application Object
    :return: None
    """

    # we need to scan the specifications package and add all yaml files.
    from importlib_resources import files
    folder = files('swagger_server.swagger')
    for _, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = folder.joinpath(file)
                _api_app.add_api(file_path)
