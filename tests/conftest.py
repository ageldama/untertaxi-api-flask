import base64

import pytest
from werkzeug.datastructures import Headers

from untertaxi_api.app_factory import create_app
from untertaxi_api.db import db
from untertaxi_api.password import hash_password
from flask import current_app


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
                                     secret_key=None):
        if secret_key is None:
            secret_key = current_app.config['SECRET_KEY']
        pw2 = hash_password(password, secret_key)
        return AuthHelpers.add_http_authz_header_base64_cleartext_password(
            headers, username, pw2)

    @staticmethod
    def add_http_authz_header_base64_cleartext_password(headers: 'Headers',
                                                        username: str, password: str):
        headers.add('Authorization',
                    'Basic ' + base64.b64encode(
                        bytes(username + ":" + password, 'ascii')).decode('ascii'))
        return headers


@pytest.fixture(scope='session')
def auth_helpers():
    return AuthHelpers()


@pytest.fixture
def faker():
    from faker import Faker
    return Faker()


@pytest.fixture
def member_driver_foo(empty_db, faker):
    from untertaxi_api.db import Member, MemberType
    email = faker.email()
    member = Member(email, 'foobarzoo', MemberType.DRIVER)
    empty_db.session.add(member)
    empty_db.session.commit()
    yield member
    empty_db.session.delete(member)
    empty_db.session.commit()


@pytest.fixture
def member_driver_bar(empty_db, faker):
    from untertaxi_api.db import Member, MemberType
    email = faker.email()
    member = Member(email, 'foobarzoo', MemberType.DRIVER)
    empty_db.session.add(member)
    empty_db.session.commit()
    yield member
    empty_db.session.delete(member)
    empty_db.session.commit()


@pytest.fixture
def member_passenger_kim(empty_db, faker):
    from untertaxi_api.db import Member, MemberType
    email = faker.email()
    member = Member(email, 'foobarzoo', MemberType.PASSENGER)
    empty_db.session.add(member)
    empty_db.session.commit()
    yield member
    empty_db.session.delete(member)
    empty_db.session.commit()


@pytest.fixture
def member_passenger_lee(empty_db, faker):
    from untertaxi_api.db import Member, MemberType
    email = faker.email()
    member = Member(email, 'foobarzoo', MemberType.PASSENGER)
    empty_db.session.add(member)
    empty_db.session.commit()
    yield member
    empty_db.session.delete(member)
    empty_db.session.commit()


@pytest.fixture
def address_passenger_kim(empty_db, member_passenger_kim, faker):
    from untertaxi_api.db import MemberAddress
    address_str = faker.address()
    address = MemberAddress(member_passenger_kim, address_str)
    empty_db.session.add(address)
    empty_db.session.commit()
    yield address
    empty_db.session.delete(address)
    empty_db.session.commit()


@pytest.fixture
def ride_request_kim(empty_db, member_passenger_kim, address_passenger_kim):
    from untertaxi_api.db import RideRequest
    ride_request = RideRequest(member_passenger_kim, address_passenger_kim)
    empty_db.session.add(ride_request)
    empty_db.session.commit()
    yield ride_request
    empty_db.session.delete(ride_request)
    empty_db.session.commit()

@pytest.fixture
def ride_request_kim_accepted_foo(empty_db, member_driver_foo, ride_request_kim):
    from untertaxi_api.db import RideRequest, RideRequestStatus
    ride_request_kim.driver_id = member_driver_foo.id
    ride_request_kim.status = RideRequestStatus.ACCEPTED
    empty_db.session.add(ride_request_kim)
    empty_db.session.commit()
    yield ride_request_kim
