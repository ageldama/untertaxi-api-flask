import base64

import pytest
from werkzeug.datastructures import Headers

from untertaxi_api.app_factory import create_app
from untertaxi_api.db import db
from untertaxi_api.password import hash_password


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


class AuthHelpers(object):
    @staticmethod
    def add_http_authz_header_base64(headers: 'Headers',
                                     username: str, password: str,
                                     secret_key: str):
        pw2 = hash_password(password, secret_key)
        headers.add('Authorization',
                    'Basic ' + base64.b64encode(
                        bytes(username + ":" + pw2, 'ascii')).decode('ascii'))
        return headers


@pytest.fixture(scope='session')
def auth_helpers():
    return AuthHelpers()
