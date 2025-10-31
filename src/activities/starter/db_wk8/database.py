""" Creates the database file with tables

Note:
    The models import is required for the create_all to create the tables.

    from activities.starter.db_wk8 import models

    """
from importlib import resources

from sqlmodel import SQLModel, create_engine, text

from activities.starter import db_wk8

student_db = resources.files(db_wk8).joinpath("students.sqlite")
sqlite_url = f"sqlite:///{str(student_db)}"
# echo=True means the SQL executed by SQLModel will be output to the terminal when the code is run.
# This can be useful for debugging.
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))  # for SQLite foreign key support
        SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)
