from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from ..password import hash_password

db = SQLAlchemy()


class Member(db.Model):
    """회원 (택시, 승객 모두)"""

    __tablename__ = 'members'

    id = db.Column('id', db.Integer, db.Sequence('members_id_seq'),
                   primary_key=True, autoincrement=True)
    email = db.Column('email', db.Unicode(200), nullable=False, unique=True)
    password_hash = db.Column('password_hash', db.Unicode(100), nullable=True)
    member_type = db.Column('member_type', db.Enum('passenger', 'driver'),
                            nullable=False)
    created_at = db.Column('created_at', db.DateTime, nullable=False,
                           default=datetime.now())
    updated_at = db.Column('updated_at', db.DateTime, nullable=False,
                           default=datetime.now(), onupdate=datetime.now())

    def __init__(self, email, password, member_type):
        self.email = email
        self.password_hash = hash_password(password, current_app.config['SECRET_KEY'])
        self.member_type = member_type

    @classmethod
    def find_first_by_email(klass, email):
        return klass.query.filter(Member.email == email).first()

    @classmethod
    def get_password_of_email(klass, email):
        member = klass.find_first_by_email(email)
        if member is None:
            return None
        else:
            return member.password
