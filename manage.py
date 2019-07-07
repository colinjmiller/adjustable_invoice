import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from adjustable_invoice import app
from adjustable_invoice.svc.base import db
from adjustable_invoice.svc.invoices.api import InvoicesAPI

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


@manager.command
def import_line_items():
    """
        Imports the line items given as sample data
    """
    with open('placements_teaser_data.json') as json_file:
        data = json.load(json_file)
        InvoicesAPI.bulk_add_line_items(data)


if __name__ == '__main__':
    manager.run()
