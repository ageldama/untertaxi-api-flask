from werkzeug.datastructures import Headers

# ---- `PUT /address`
from untertaxi_api.db import MemberAddress

# ---- `GET /address/<address_id>`


def test_get_address_not_found(flask_client, auth_helpers, empty_db,
                               address_passenger_kim, member_passenger_kim):
    resp = flask_client.get('/v1/address/' + str(address_passenger_kim.id * 3),
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 400


def test_get_address_no_owner_ok(flask_client, auth_helpers, empty_db,
                                 address_passenger_kim, member_passenger_kim, member_driver_foo):
    resp = flask_client.get('/v1/address/' + str(address_passenger_kim.id),
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 200
    assert 'id' in resp.json
    assert resp.json['id'] == address_passenger_kim.id
    assert 'created_at' in resp.json
    assert 'updated_at' in resp.json
    assert 'active' in resp.json
    assert 'address' in resp.json
    assert resp.json['address'] == address_passenger_kim.address
    assert 'member_id' in resp.json
    assert resp.json['member_id'] == member_passenger_kim.id
    assert resp.json['member_id'] != member_driver_foo.id


def test_get_address_access_denied(flask_client, auth_helpers, empty_db,
                                   address_passenger_kim):
    resp = flask_client.get('/v1/address/' + str(address_passenger_kim.id))
    assert resp.status_code == 401


def test_address_new_ok(flask_client, auth_helpers, member_passenger_kim, empty_db, faker):
    resp = flask_client.put('/v1/address',
                            json={
                                'address': faker.address()
                            },
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 200
    assert 'id' in resp.json
    # cleanup
    address = MemberAddress.query.get(resp.json['id'])
    empty_db.session.delete(address)
    empty_db.session.commit()


def test_address_new_access_denied(flask_client, auth_helpers, faker):
    resp = flask_client.put('/v1/address',
                            json={
                                'address': faker.address()
                            })
    assert resp.status_code == 401


def test_address_new_empty_body(flask_client, auth_helpers, member_passenger_kim):
    resp = flask_client.put('/v1/address',
                            json={},
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 400


def test_address_new_too_short(flask_client, auth_helpers, member_passenger_kim):
    resp = flask_client.put('/v1/address',
                            json={'address': ''},
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 400


def test_address_new_too_short(flask_client, auth_helpers, member_passenger_kim):
    resp = flask_client.put('/v1/address',
                            json={'address': '.' * 200},
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 400

# --- `GET /address`


def test_address_list_empty(flask_client, auth_helpers, member_driver_foo):
    resp = flask_client.get('/v1/address',
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 200
    assert len(resp.json) == 0


def test_address_list_access_denied(flask_client):
    resp = flask_client.get('/v1/address')
    assert resp.status_code == 401


def test_address_list_ok(flask_client, auth_helpers, member_passenger_kim, address_passenger_kim):
    resp = flask_client.get('/v1/address',
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 200
    assert len(resp.json) > 0

# ---- `DELETE /address/<address_id>`


def test_address_deactivate_access_denied(flask_client, auth_helpers, member_passenger_kim, address_passenger_kim):
    resp = flask_client.delete('/v1/address/' + str(address_passenger_kim.id))
    assert resp.status_code == 401


def test_address_deactivate_ok(flask_client, auth_helpers, member_passenger_kim, address_passenger_kim):
    resp = flask_client.delete('/v1/address/' + str(address_passenger_kim.id),
                               headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 204
    assert not MemberAddress.query.get(address_passenger_kim.id).active


def test_address_deactivate_not_found(flask_client, auth_helpers, member_passenger_kim, address_passenger_kim):
    resp = flask_client.delete('/v1/address/' + str(address_passenger_kim.id * 3),
                               headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 400


def test_address_deactivate_not_owner(flask_client, auth_helpers, member_driver_foo, address_passenger_kim):
    resp = flask_client.delete('/v1/address/' + str(address_passenger_kim.id),
                               headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 401
