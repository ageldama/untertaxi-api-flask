"""
Basic "Hello!" API blueprint.
"""
from flask import Blueprint
from ...auth import auth


BP = Blueprint('hello', __name__,
               template_folder='templates')


@BP.route('/')
def index():
    """Nothing is more simple
    ---
    responses:
      200:
        description: A nice greeting message in text/html
    """
    return "Hello!"


@BP.route('/restricted')
@auth.login_required
def restricted():
    """Hello but login-required.
    ---
    tags:
      - login-required-restricted
    responses:
      200:
        description: A nice greeting message in text/html
    """
    return "Hello! ???"
