import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import query
    app.register_blueprint(query.bp)

    @app.route('/')
    def hello():
        return 'Hello World!'

    return app
