from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager


db = SQLAlchemy()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.create_scoped_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

from .users.models import User
