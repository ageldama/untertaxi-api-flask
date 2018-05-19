from faker import Faker
from pytest import raises
from sqlalchemy.exc import IntegrityError

from untertaxi_api.db import Member, MemberType, db


f = Faker()


def test_insert_new_member(empty_db):
    m = Member(f.email(), 'foobarzoo', MemberType.PASSENGER)
    db.session.add(m)
    db.session.commit()


def test_insert_new_member_existing(empty_db):
    email = f.email()
    with raises(IntegrityError):
        m1 = Member(email, 'foobarzoo', MemberType.PASSENGER)
        db.session.add(m1)
        m2 = Member(email, 'foobarzoo', MemberType.PASSENGER)
        db.session.add(m2)
        db.session.commit()
