from datetime import datetime
from enum import Enum

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey

from ..password import hash_password

db = SQLAlchemy()


class MemberType(Enum):
    "회원 타입: 승객or기사"
    PASSENGER = 'PASSENGER'
    DRIVER = 'DRIVER'


class Member(db.Model):
    """회원 (택시, 승객 모두)"""

    __tablename__ = 'members'

    id = db.Column('id', db.Integer, db.Sequence('members_id_seq'),
                   primary_key=True, autoincrement=True)
    email = db.Column('email', db.Unicode(200), nullable=False, unique=True)
    password_hash = db.Column('password_hash', db.Unicode(100), nullable=True)
    member_type = db.Column('member_type',
                            db.Enum(MemberType, name='member_type'),
                            nullable=False)
    created_at = db.Column('created_at', db.DateTime, nullable=False,
                           default=datetime.now())
    updated_at = db.Column('updated_at', db.DateTime, nullable=False,
                           default=datetime.now(), onupdate=datetime.now())
    active = db.Column('is_active', db.Boolean(), nullable=False, default=True)

    # ---- constructor ----

    def __init__(self, email: str, password: str, member_type: str):
        self.email = email
        self.password_hash = hash_password(
            password, current_app.config['SECRET_KEY'])
        self.member_type = member_type

    # ---- JSON ----

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'member_type': self.member_type.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'active': self.active
        }

    # ---- 데이터 접근용 ----

    @classmethod
    def find_first_by_email(cls, email):
        return cls.query.filter(Member.email == email,
                                Member.active == True).first()

    @classmethod
    def count_by_email(cls, email):
        return cls.query.filter(Member.email == email).count()

    @classmethod
    def get_password_of_email(cls, email):
        member = cls.find_first_by_email(email)
        if member is None:
            return None
        return member.password_hash


class MemberAddress(db.Model):
    "배차 요청 승객의 주소"
    __tablename__ = 'member_addresses'

    id = db.Column('id', db.Integer, db.Sequence('member_addresses_id_seq'),
                   primary_key=True, autoincrement=True)
    member_id = db.Column('member_id', db.Integer, ForeignKey(Member.id),
                          nullable=False)
    address = db.Column('address', db.Unicode(100), nullable=False)
    created_at = db.Column('created_at', db.DateTime, nullable=False,
                           default=datetime.now())
    updated_at = db.Column('updated_at', db.DateTime, nullable=False,
                           default=datetime.now(), onupdate=datetime.now())
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       default=True, server_default="true")

    # ---- backrefs ----
    member = relationship('Member', backref=backref(
        'member_addresses'), uselist=False)

    # ---- constructor ----

    def __init__(self, member: 'Member', address: str):
        self.address = address
        self.member_id = member.id

    # ---- JSON ----

    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'active': self.active
        }

    # ---- 데이터 접근용 ----

    @classmethod
    def find_all_by_email(cls, email):
        member = Member.find_first_by_email(email)
        assert member is not None
        return MemberAddress.query.filter(
            MemberAddress.member_id == member.id,
            MemberAddress.active == True
        ).order_by(MemberAddress.created_at).all()

    @classmethod
    def deactivate(cls, address_id):
        MemberAddress.query.filter(
            MemberAddress.id == address_id
        ).update({MemberAddress.active: False},
                 synchronize_session=False)
        db.session.commit()


class RideRequestStatus(Enum):
    "배차요청상태"
    AVAILABLE = "AVAILABLE"  # 배차요청하여 대기중.
    ACCEPTED = "ACCEPTED"  # 배차성공.
    ARRIVED = "ARRIVED"  # 배차받아 도착완료.


class RideRequest(db.Model):
    __tablename__ = 'ride_requests'
    id = db.Column('id', db.Integer, db.Sequence('ride_requests_id_seq'),
                   primary_key=True, autoincrement=True)
    passenger_id = db.Column('passenger_id', db.Integer,
                             ForeignKey(Member.id),
                             nullable=False)
    driver_id = db.Column('driver_id', db.Integer,
                          ForeignKey(Member.id),
                          nullable=True)
    address_id = db.Column('address_id', db.Integer,
                           ForeignKey(MemberAddress.id),
                           nullable=False)
    created_at = db.Column('created_at', db.DateTime, nullable=False,
                           default=datetime.now())
    updated_at = db.Column('updated_at', db.DateTime, nullable=False,
                           default=datetime.now(), onupdate=datetime.now())
    status = db.Column('status',
                       db.Enum(RideRequestStatus, name='ride_request_status'),
                       nullable=False, default=RideRequestStatus.AVAILABLE)

    # ---- JSON ----

    def to_dict(self):
        return {
            'id': self.id,
            'passenger_id': self.passenger_id,
            'driver_id': self.driver_id,
            'address_id': self.address_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status.name
        }

    # ---- constructor ----

    def __init__(self, passenger: 'Member', address: 'MemberAddress'):
        self.passenger_id = passenger.id
        self.address_id = address.id

    # ---- 데이터 접근용 ----

    @classmethod
    def find_all(cls):
        return RideRequest.query.order_by(
            RideRequest.created_at.desc()).all()

    @classmethod
    def deactivate(cls, ride_request_id):
        RideRequest.query.filter(
            RideRequest.id == ride_request_id
        ).update({RideRequest.active: False},
                 synchronize_session=False)
        db.session.commit()
