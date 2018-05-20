from pytest import raises
from sqlalchemy.exc import IntegrityError

from untertaxi_api.db import Member, MemberType, db


def test_insert_new_member(empty_db, faker):
    m = Member(faker.email(), 'foobarzoo', MemberType.PASSENGER)
    db.session.add(m)
    db.session.commit()


def test_insert_new_member_existing(empty_db, faker):
    email = faker.email()
    with raises(IntegrityError):
        m1 = Member(email, 'foobarzoo', MemberType.PASSENGER)
        db.session.add(m1)
        m2 = Member(email, 'foobarzoo', MemberType.PASSENGER)
        db.session.add(m2)
        db.session.commit()
