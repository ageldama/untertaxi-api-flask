"""
Create and Initialize new Flask app instance.
"""
from __future__ import print_function
import sys
from os import environ
import pprint
from flask import Flask
from .blueprints import hello


def create_app():
    """Create new flask app object from blueprints with a configuration"""
    app = Flask('untertaxi_api')
    load_settings(app)
    app.register_blueprint(hello.BP, url_prefix='/hello')
    app.logger.debug("INITED!")
    #
    return app


def load_settings(app):
    """Load default configuration
    and if `UNTERTAXI_API_CONFIG_FILE`-envvar has specified,
    load from the specified config-file and update.
    """
    app.config.from_object('untertaxi_api.config.DefaultSettings')
    puts_console("Default settings -- {}".format(pprint.pformat(app.config)))
    env_name = 'UNTERTAXI_API_CONFIG_FILE'
    env_specified = env_name in environ
    puts_console('(Configuration filename with env) {} specified? {}'.format(
        env_name, env_specified))
    if env_specified:
        app.config.from_envvar(env_name)
        puts_console("Settings after the merged with {} -- {}".format(
            environ[env_name],
            pprint.pformat(app.config)))
    puts_console("Secret key -- {}".format(app.config['SECRET_KEY']))


def puts_console(msg):
    """Poor man's logging: because don't have real logger not yet here."""
    print(msg, file=sys.stderr)
