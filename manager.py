#!/usr/bin/env python
from flask_migrate import MigrateCommand
from flask_script import Manager
from lem import create_app

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.option('-p', dest='password', help='User password', required=True)
@manager.option('-e', dest='email', help='User email', required=True)
def create_user(email, password):
    from lem import business
    business.create_user(email, password)
    print('User {} created'.format(email))

if __name__ == '__main__':
    manager.run()
