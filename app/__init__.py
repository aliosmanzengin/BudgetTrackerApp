# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()


def create_app() -> Flask:
    """
    Creates and configures the Flask application with a database connection
    and registered blueprints.

    Configurations:
        - SQLALCHEMY_DATABASE_URI: Database URI for SQLAlchemy.
        - SQLALCHEMY_TRACK_MODIFICATIONS: Disable to avoid overhead.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()

    return app
