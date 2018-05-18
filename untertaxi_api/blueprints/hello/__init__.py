"""
Basic "Hello!" API blueprint.
"""
from flask import Blueprint
from ...auth import auth


BP = Blueprint('hello', __name__,
               template_folder='templates')


@BP.route('/')
def index():
    "Nothing is more simple"
    return "Hello!"


@BP.route('/restricted')
@auth.login_required
def restricted():
    return "Hello! ???"
