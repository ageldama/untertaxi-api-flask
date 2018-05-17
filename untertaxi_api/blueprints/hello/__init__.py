"""
Basic "Hello!" API blueprint.
"""
from flask import Blueprint


BP = Blueprint('hello', __name__,
               template_folder='templates')


@BP.route('/')
def index():
    "Nothing is more simple"
    return "Hello!"
