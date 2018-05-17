#!/usr/bin/env python
# -*- coding: utf-8; -*-
from flask_script import Manager, Shell
from flask_script.commands import ShowUrls
from untertaxi_api.app_factory import create_app


app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('show_urls', ShowUrls)


if __name__ == '__main__':
    manager.run()
