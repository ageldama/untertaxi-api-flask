import pytest
from untertaxi_api.app_factory import create_app
from untertaxi_api.db import db


@pytest.fixture(scope='session')
def flask_app():
    "Flask app instance fixture."
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture(scope='session')
def flask_client(flask_app):
    "Flask test client fixture."
    return flask_app.test_client()


@pytest.fixture
def empty_db(flask_app):
    db.create_all()
    return db
