import os

from flask import Flask, redirect, jsonify, url_for

from .middleware.prefix import PrefixMiddleware


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if 'env' in os.environ and os.environ['env'] == 'qa':
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/gaql')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import views

    app.register_blueprint(views.bp)

    @app.route('/health')
    def health():
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

    return app
