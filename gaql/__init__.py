import os

from flask import Flask, redirect, jsonify, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

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

    @app.context_processor
    def prefix_paths():
        path_prefix = os.getenv('PATH_PREFIX')
        if path_prefix:
            return dict(path_prefix=path_prefix)
        return dict()

    return app
