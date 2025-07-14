from app.config import DatabaseSQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, text

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                query = db.execute(select(self.model))
                return query.scalars().all()
        except SQLAlchemyError as e:
            print(f"Error fetching all: {e}")
            raise

    def get_by_id(self, id):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                query = db.execute(select(self.model).where(self.model.id == id))
                return query.scalars().first()
        except SQLAlchemyError as e:
            print(f"Error fetching by id: {e}")
            raise

    def find_all_by(self, **kwargs):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                conditions = [getattr(self.model, k) == v for k, v in kwargs.items()]
                query = db.execute(select(self.model).where(*conditions))
                return query.scalars().all()
        except SQLAlchemyError as e:
            print(f"Error in find_all_by: {e}")
            raise

    def find_first_by(self, **kwargs):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                conditions = [getattr(self.model, k) == v for k, v in kwargs.items()]
                query = db.execute(select(self.model).where(*conditions))
                return query.scalars().first()
        except SQLAlchemyError as e:
            print(f"Error in find_first_by: {e}")
            raise

    def save(self, entity):
        self.before_save(entity)
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                db.add(entity)
                db.commit()
                self.after_save(entity)
                return entity
        except SQLAlchemyError as e:
            print(f"Error saving entity: {e}")
            raise

    def delete(self, entity):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                db.delete(entity)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error deleting entity: {e}")
            raise

    def count(self):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                return db.query(self.model).count()
        except SQLAlchemyError as e:
            print(f"Error counting entities: {e}")
            raise

    def count_by(self, **kwargs):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                query = db.query(self.model).filter_by(**kwargs)
                return query.count()
        except SQLAlchemyError as e:
            print(f"Error in count_by: {e}")
            raise

    def update(self, entity, **kwargs):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                for attr, value in kwargs.items():
                    setattr(entity, attr, value)
                db.commit()
                print(entity.to_dict())
                return entity
        except SQLAlchemyError as e:
            print(f"Error updating entity: {e}")
            raise

    def bulk_save(self, entities):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                db.add_all(entities)
                db.commit()
                return entities
        except SQLAlchemyError as e:
            print(f"Error in bulk save: {e}")
            raise

    def bulk_delete(self, entities):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                for entity in entities:
                    db_entity = db.get(self.model, entity.id)
                    if db_entity is not None:
                        db.delete(db_entity)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error in bulk delete: {e}")
            raise

    def find_by_criteria(self, *criterion):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                query = db.execute(select(self.model).where(*criterion))
                return query.scalars().all()
        except SQLAlchemyError as e:
            print(f"Error in find_by_criteria: {e}")
            raise

    def get_all_ordered(self, order_by, descending=False):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                order_clause = order_by.desc() if descending else order_by
                query = db.execute(select(self.model).order_by(order_clause))
                return query.scalars().all()
        except SQLAlchemyError as e:
            print(f"Error in get_all_ordered: {e}")
            raise

    def execute_raw_sql(self, sql, params=None):
        try:
            with DatabaseSQLAlchemy.get_db() as db:
                result = db.execute(text(sql), params or {})
                db.commit()
                return result
        except SQLAlchemyError as e:
            print(f"Error executing raw SQL: {e}")
            raise

    def before_save(self, entity):
        return entity

    def after_save(self, entity):
        return entity

    def validate(self, entity):
        if hasattr(entity, "email") and "@" not in entity.email:
            raise ValueError("Invalid email address.")
        return True

    def _validate_name(self, name: str):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        if len(name) > 255:
            raise ValueError("Name is too long.")
        if ";" in name or "--" in name:
            raise ValueError("Invalid characters in name.")
