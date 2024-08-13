import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def get_db():
    """
    Return SLQAlcmemy object.
    """
    return db


def close_db():
    """
    Closes all database sessions.
    """
    db.close_all_sessions()


def init_db():
    """
    Clear existing data and create new tables.
    """
    with current_app.app_context():
        db.create_all()


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
    app.cli.add_command(init_db_command)
    db.init_app(app)
