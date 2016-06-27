from flask_script import Manager, \
                        Shell
from flask_migrate import Migrate, \
                        MigrateCommand

from bookcrossing import app, db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db
}))


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
