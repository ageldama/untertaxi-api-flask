"""
Create and Initialize new Flask app instance.
"""
from __future__ import print_function
import sys
from os import getenv
from flask import Flask
from .blueprints import hello
from .config import CONFIGS
from .db import db


def create_app(profile=''):
    """Create new flask app object from blueprints with a configuration"""
    app = Flask('untertaxi_api')
    env_name = 'UNTERTAXI_API_CONFIG'
    load_settings(app, getenv(env_name) or profile)
    db.init_app(app=app)
    app.register_blueprint(hello.BP, url_prefix='/hello')
    app.logger.debug("INITED!")
    #
    return app


def load_settings(app, profile):
    """Load default configuration
    and if `UNTERTAXI_API_CONFIG`-envvar has specified,
    use specified configuration profile.
    """
    puts_console('profile name = <{}>'.format(profile))
    if len(profile) > 0:
        app.config.from_object(CONFIGS[profile])
    else:
        app.config.from_object('untertaxi_api.config.LocalhostSettings')

        
def puts_console(msg):
    """Poor man's logging: because don't have real logger not yet here."""
    print(msg, file=sys.stderr)
