from sqlalchemy.exc import IntegrityError

from exceptions import ConflictError
from extensions import db


class BaseRepository:
    """Acceso a datos genérico. Los servicios no tocan la sesión de SQLAlchemy directamente."""

    model = None

    def __init__(self, session=None):
        self.session = session or db.session

    def get(self, entity_id):
        return self.session.get(self.model, entity_id)

    def add(self, entity):
        self.session.add(entity)
        return entity

    def delete(self, entity):
        self.session.delete(entity)

    def commit(self):
        """Confirma la transacción; una violación de integridad se informa como ConflictError."""
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise ConflictError() from e
        except Exception:
            self.session.rollback()
            raise

    @staticmethod
    def paginate(query, limit=None, offset=0, max_limit=500):
        if limit is None:
            return query
        return query.limit(min(max(limit, 1), max_limit)).offset(max(offset, 0))
