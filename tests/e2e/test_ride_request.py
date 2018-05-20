from werkzeug.datastructures import Headers
from untertaxi_api.db import RideRequest, RideRequestStatus

# --- `GET /ride_request` ----


def test_ride_request_get_access_denied(flask_client, ride_request_kim):
    resp = flask_client.get('/v1/ride_request')
    assert resp.status_code == 401


def test_ride_request_get_ok(flask_client, auth_helpers, ride_request_kim, member_driver_foo):
    resp = flask_client.get('/v1/ride_request',
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 200
    assert resp.json is not None and len(resp.json) > 0
    ride_request = resp.json[0]
    assert 'address_id' in ride_request
    assert 'created_at' in ride_request
    assert 'updated_at' in ride_request
    assert 'driver_id' in ride_request
    assert 'passenger_id' in ride_request
    assert 'status' in ride_request

# ---- `DELETE /ride_request/<ride_request_id>` ----


def test_ride_request_deactivate_access_denied(flask_client, ride_request_kim):
    resp = flask_client.delete('/v1/ride_request/' + str(ride_request_kim.id))
    assert resp.status_code == 401


def test_ride_request_deactivate_not_found(flask_client, ride_request_kim,
                                           auth_helpers, member_passenger_kim):
    resp = flask_client.delete('/v1/ride_request/' + str(ride_request_kim.id * 3),
                               headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 400


def test_ride_request_deactivate_not_owner(flask_client, ride_request_kim,
                                           auth_helpers, member_driver_foo):
    resp = flask_client.delete('/v1/ride_request/' + str(ride_request_kim.id),
                               headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 401


def test_ride_request_deactive_ok(flask_client, ride_request_kim,
                                  auth_helpers, member_passenger_kim):
    resp = flask_client.delete('/v1/ride_request/' + str(ride_request_kim.id),
                               headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 204
    assert RideRequest.query.get(
        ride_request_kim.id).status == RideRequestStatus.CANCELLED

# ---- `POST /ride_request/<ride_request_id>/accept` ----


def test_ride_request_accept_not_found(flask_client, ride_request_kim,
                                       auth_helpers, member_driver_foo):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim.id * 3) + '/accept',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 400


def test_ride_request_accept_access_denied(flask_client, ride_request_kim):
    resp = flask_client.post('/v1/ride_request/' +
                             str(ride_request_kim.id) + '/accept')
    assert resp.status_code == 401


def test_ride_request_accept_no_self_accepting(flask_client, ride_request_kim,
                                               member_passenger_kim, auth_helpers):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim.id) + '/accept',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 401


def test_ride_request_accept_only_can_by_drivers(flask_client, ride_request_kim,
                                                 auth_helpers,
                                                 member_passenger_kim, member_passenger_lee):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim.id) + '/accept',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_passenger_lee.email, member_passenger_lee.password_hash))
    assert resp.status_code == 401


def test_ride_request_accept_ok(flask_client, ride_request_kim,
                                auth_helpers,
                                member_driver_foo):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim.id) + '/accept',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 204
    assert RideRequestStatus.ACCEPTED == RideRequest.query.get(
        ride_request_kim.id).status


# ---- `POST /ride_request/<ride_request_id>/arrive` ----

def test_ride_request_arrive_ok(flask_client, ride_request_kim_accepted_foo,
                                auth_helpers, member_driver_foo):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim_accepted_foo.id) + '/arrive',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 204


def test_ride_request_arrive_access_denied(flask_client, ride_request_kim_accepted_foo):
    resp = flask_client.post('/v1/ride_request/' +
                             str(ride_request_kim_accepted_foo.id) + '/arrive')
    assert resp.status_code == 401


def test_ride_request_arrive_not_found(flask_client, ride_request_kim_accepted_foo,
                                       auth_helpers, member_driver_foo):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim_accepted_foo.id * 3) + '/arrive',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_driver_foo.email, member_driver_foo.password_hash))
    assert resp.status_code == 400


def test_ride_request_arrive_not_driver(flask_client, ride_request_kim_accepted_foo,
                                        auth_helpers, member_passenger_lee):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim_accepted_foo.id * 3) + '/arrive',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_passenger_lee.email, member_passenger_lee.password_hash))
    assert resp.status_code == 401


def test_ride_request_arrive_not_other_driver(flask_client, ride_request_kim_accepted_foo,
                                              auth_helpers, member_driver_bar):
    resp = flask_client.post('/v1/ride_request/' + str(ride_request_kim_accepted_foo.id) + '/arrive',
                             headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
        Headers(), member_driver_bar.email, member_driver_bar.password_hash))
    assert resp.status_code == 401


# ---- `PUT /ride_request` ----

def test_ride_request_new_ok(flask_client, auth_helpers,
                             empty_db,
                             member_passenger_kim, address_passenger_kim):
    resp = flask_client.put('/v1/ride_request',
                            json={
                                'address_id': address_passenger_kim.id
                            },
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 200
    assert 'id' in resp.json
    ride_request = RideRequest.query.get(resp.json['id'])
    empty_db.session.delete(ride_request)
    empty_db.session.commit()


def test_ride_request_new_address_not_found(flask_client, auth_helpers,
                                            empty_db,
                                            member_passenger_kim, address_passenger_kim):
    resp = flask_client.put('/v1/ride_request',
                            json={
                                'address_id': 3 * address_passenger_kim.id
                            },
                            headers=auth_helpers.add_http_authz_header_base64_cleartext_password(
                                Headers(), member_passenger_kim.email, member_passenger_kim.password_hash))
    assert resp.status_code == 400


def test_ride_request_new_access_denied(flask_client, auth_helpers,
                                        address_passenger_kim):
    resp = flask_client.put('/v1/ride_request',
                            json={
                                'address_id': address_passenger_kim.id
                            })
    assert resp.status_code == 401
