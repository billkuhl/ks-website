#!/usr/bin/env python
import os
import subprocess
import pandas

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from web import app
from web import db
from web.config import *
from web.models import Role, User

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name="Administrator")
    if admin_query.first() is not None:
        if User.query.filter_by(email=ADMIN_EMAIL).first() is None:
            user = User(
                first_name="Admin",
                last_name="Account",
                password=ADMIN_PASSWORD,
                confirmed=True,
                email=ADMIN_EMAIL,
                beer_code="0000",
            )
            db.session.add(user)
            db.session.commit()
            print("Added administrator {}".format(user.full_name()))


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def reset():
    """
    Recreates the database and adds the admin user
    """
    recreate_db()
    setup_dev()


@manager.command
def add_brothers_from_csv():
    df = pandas.read_csv("./KS Brotherhood Info.csv")
    for ind in df.index:
        name = str(df["Name"][ind])
        class_year = int(df["Class Year"][ind])
        rook_number = int(df["Rook Number"][ind])

        name_parts = name.split()
        if len(name_parts) == 2:
            first_name = name_parts[0]
            middle_initial = ""
            last_name = name_parts[1]
        else:
            first_name = name_parts[0]
            middle_initial = name_parts[1][0]
            last_name = " ".join(name_parts[2:])

        User.add_brother(first_name, middle_initial, last_name, class_year, rook_number)
    return


@manager.option(
    "-n",
    "--number-users",
    default=10,
    type=int,
    help="Number of each model type to create",
    dest="number_users",
)
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    print("huh")
    User.generate_fake(count=number_users)


if __name__ == "__main__":
    manager.run()
