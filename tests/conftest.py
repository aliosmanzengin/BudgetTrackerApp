# tests/conftest.py
import pytest
from app import create_app, db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Configure the app for testing
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing

    # Create a test client using the Flask application
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()  # Create the database tables
        yield testing_client  # Yield the test client for use in tests

    # Cleanup after tests
    with flask_app.app_context():
        db.drop_all()
