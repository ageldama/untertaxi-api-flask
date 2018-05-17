#!/usr/bin/env python
# -*- coding: utf-8; -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_script.commands import ShowUrls

from untertaxi_api.app_factory import create_app
from untertaxi_api.db import db


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('show_urls', ShowUrls)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
