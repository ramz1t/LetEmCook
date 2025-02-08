from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

Base = declarative_base()
engine = create_engine('sqlite:///letemcook.db')
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_scope():
    """
    Context manager for transactional database sessions.
    Ensures sessions are committed or rolled back and closed properly.

    Usage:
    with session_scope() as session:
        # Perform database operations
        session.add(new_record)

    Yields:
    session: SQLAlchemy session object

    Raises:
    Exception: Rolls back session on error
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
