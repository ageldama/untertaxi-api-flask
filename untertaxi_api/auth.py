from flask_httpauth import HTTPBasicAuth

from .db import Member, db

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(email):
    return Member.get_password_of_email(email)


def init_app(app):
    # Do nothing but return it.
    return app
