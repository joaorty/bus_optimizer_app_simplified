from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from sqlalchemy.inspection import inspect
from contextlib import contextmanager

metadata = MetaData()

class Base(DeclarativeBase):
    __abstract__ = True
    metadata = metadata

    def to_dict(self):
        mapper = inspect(self).mapper
        return {
            column.key: getattr(self, column.key, None)
            for column in self.__table__.columns
        }

class DatabaseSQLAlchemy:
    _db = None

    @staticmethod
    def get_db():
        if not DatabaseSQLAlchemy._db:
            DatabaseSQLAlchemy._db = SQLAlchemy(model_class=Base)
        return DatabaseSQLAlchemy._db

    @staticmethod
    def init_app(app):
        if not DatabaseSQLAlchemy._db:
            DatabaseSQLAlchemy._db = SQLAlchemy(model_class=Base)
        DatabaseSQLAlchemy._db.init_app(app)

    @staticmethod
    def reset_db():
        sqlalchemy = DatabaseSQLAlchemy.get_db()
        with sqlalchemy.engine.connect() as conn:
            conn.execute("DROP SCHEMA IF EXISTS public CASCADE;")
            conn.execute("CREATE SCHEMA public;")
            sqlalchemy.session.commit()
