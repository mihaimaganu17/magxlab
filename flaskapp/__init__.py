import os

from flask import Flask

CWD = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(CWD, "storage")

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE = os.path.join(app.instance_path, "magxlab.sqlite"),
    )

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)


    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return "Hello, World"

    from . import db

    # Initialize the database for this application
    db.init_app(app)

    from . import sample

    # Register the sample blueprint in the main app
    app.register_blueprint(sample.bp)

    return app
