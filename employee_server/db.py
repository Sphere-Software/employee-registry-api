import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def get_db():
    """
    Return SLQAlcmemy object.
    """
    return db


def init_db(app):
    """
    Clear existing data and create new tables.
    """
    with app.app_context():
        db.create_all()


def init_app(app):
    """
    Register database functions with Flask app. This called by the application
    factory.
    """
    db.init_app(app)
    init_db(app)
    app.logger.info("Application initialised.")
