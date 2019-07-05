from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from adjustable_invoice import app
from adjustable_invoice.svc.base import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """
    Recreates a database. This should only be used once
    when there's a new database instance. This shouldn't be
    used when you migrate your database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    manager.run()
