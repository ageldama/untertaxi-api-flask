# -*- coding: utf-8; -*-
"""
Configuration object definition.
"""


class LocalhostSettings(object):
    """Default Configuration"""
    SECRET_KEY = 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@127.0.0.1:5432/untertaxi_api'
    TESTING = False
    DEBUG = True


class DockerSettings(object):
    """Docker Configuration"""
    SECRET_KEY = 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@db:5432/untertaxi_api'
    TESTING = False
    DEBUG = False


class TestingSettings(LocalhostSettings):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


CONFIGS = {
    'localhost': LocalhostSettings(),
    'docker': DockerSettings(),
    'testing': TestingSettings(),
}
