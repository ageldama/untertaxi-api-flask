from unittest.mock import ANY, patch

from flask import current_app
from werkzeug.datastructures import Headers

from untertaxi_api.db import Member
from untertaxi_api.password import hash_password


def test_hello(flask_client):
    "Test `GET /hello/` endpoint"
    assert flask_client is not None
    resp = flask_client.get('/hello/')
    assert resp.status_code == 200


def test_restricted(flask_client, auth_helpers):
    "Test `GET /hello/restricted` endpoint"
    assert flask_client is not None
    # access denied
    resp = flask_client.get('/hello/restricted')
    assert resp.status_code == 401
    # login ok
    username = 'foo'
    password = 'bar'
    #
    pw2 = hash_password(password, current_app.config['SECRET_KEY'])
    with patch.object(Member, 'get_password_of_email', return_value=pw2):
        resp = flask_client.get('/hello/restricted',
                                headers=auth_helpers.add_http_authz_header_base64(
                                    Headers(), username, password))
        assert resp.status_code == 200
        Member.get_password_of_email.assert_called_once_with(username)


def test_no_mocker(empty_db):
    import uuid
    username = str(uuid.uuid4())
    assert Member.get_password_of_email(username) is None

# EOF.
