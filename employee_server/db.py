import sqlite3

import click
from flask import current_app
from flask import g


def get_db():
    """
    Connect to the application's configured database. The connection is unique
    for each request and will be reused if called again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    If this request is connected to the database, close the connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Clear existing data and create new tables.
    """
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """
    Clear existing data and create new tables.
    """
    init_db()
    click.echo("Initialised the database")


def init_app(app):
    """
    Register database functions with Flask app. This called by the application
    factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.__setattr__("get_db", get_db)
