from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey

from ..password import hash_password
import enum

db = SQLAlchemy()


class MemberType(enum.Enum):
    passenger = 'passenger'
    driver = 'driver'


class Member(db.Model):
    """회원 (택시, 승객 모두)"""

    __tablename__ = 'members'

    id = db.Column('id', db.Integer, db.Sequence('members_id_seq'),
                   primary_key=True, autoincrement=True)
    email = db.Column('email', db.Unicode(200), nullable=False, unique=True)
    password_hash = db.Column('password_hash', db.Unicode(100), nullable=True)
    member_type = db.Column('member_type',
                            db.Enum(MemberType, name='member_type'), nullable=False)
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

    # ---- 데이터 접근용 ----

    @classmethod
    def find_first_by_email(klass, email):
        return klass.query.filter(Member.email == email,
                                  Member.active == True).first()

    @classmethod
    def get_password_of_email(klass, email):
        member = klass.find_first_by_email(email)
        if member is None:
            return None
        else:
            return member.password


class MemberAddress(db.Model):
    "배차 요청 승객의 주소"
    __tablename__ = 'member_addresses'

    id = db.Column('id', db.Integer, db.Sequence('members_id_seq'),
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
    member = relationship('Member', backref=backref('member_addresses'), uselist=False)

    # ---- constructor ----

    def __init__(self, member: 'Member', address: str):
        self.address = address
        self.member_id = member.id


