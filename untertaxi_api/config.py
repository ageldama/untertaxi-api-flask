# -*- coding: utf-8; -*-
"""
Configuration object definition.
"""


class LocalhostSettings(object):
    """Default Configuration"""
    SECRET_KEY = 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///untertaxi.sqlite'
    TESTING = False
    DEBUG = True


class TestingSettings(LocalhostSettings):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


CONFIGS = {
    'localhost': LocalhostSettings(),
    'testing': TestingSettings(),
}
