from untertaxi_api.db import MemberType
from werkzeug.datastructures import Headers


# ---- `PUT /member`

def test_signup_email_fail(flask_client, auth_helpers, empty_db):
    resp = flask_client.put('/v1/member', json={
        'email': 'foo'
    })
    assert resp.status_code == 400


def test_signup_ok(flask_client, auth_helpers, empty_db):
    resp = flask_client.put('/v1/member', json={
        'email': 'foo@bar.com',
        'password': 'foobarzoospam',
        'member_type': 'DRIVER'
    })
    assert resp.status_code == 201


def test_signup_email_existing(flask_client, auth_helpers, empty_db, member_driver_foo):
    resp = flask_client.put('/v1/member', json={
        'email': member_driver_foo.email,
        'password': 'foobarzoospam',
        'member_type': 'DRIVER'
    })
    assert resp.status_code == 400


def test_signup_password_fail(flask_client, auth_helpers, empty_db):
    resp = flask_client.put('/v1/member', json={
        'email': 'foo@bar.com'
    })
    assert resp.status_code == 400


def test_signup_empty_request(flask_client, auth_helpers, empty_db):
    resp = flask_client.put('/v1/member')
    assert resp.status_code == 500


# ---- `GET /member/<member_id>`

def test_get_member_not_existing(flask_client, auth_helpers, empty_db, member_driver_foo):
    resp = flask_client.get('/v1/member/1234567',
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 400


def test_get_member_ok(flask_client, auth_helpers, empty_db, member_driver_foo):
    resp = flask_client.get('/v1/member/' + str(member_driver_foo.id),
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert 'active' in resp.json
    assert 'created_at' in resp.json
    assert 'updated_at' in resp.json
    assert 'email' in resp.json
    assert 'password' not in resp.json
    assert 'password_hash' not in resp.json
    assert resp.json['email'] == member_driver_foo.email
    assert MemberType(resp.json['member_type']
                      ) == member_driver_foo.member_type
    assert resp.status_code == 200
