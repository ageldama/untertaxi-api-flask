from flask_httpauth import HTTPBasicAuth

from .db import Member, db

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(email):
    m = Member.query.filter(Member.email == email).first()
    if m is not None:
        return m.password
    else:
        return None


def init_app(app):
    # Do nothing but return it.
    return app
