import pytest
from app.models import Base, engine, Session, Note
from app.controllers.NotesController import NotesController


@pytest.fixture(scope="function")
def setup_database():
    """
    Setup a clean database for each test, creating test data and returning it.
    Yields the test database session.
    """

    Base.metadata.create_all(engine)

    with Session() as session:
        try:
            note1 = Note(title="Sample Title 1", text="Sample Text 1")
            note2 = Note(title="Sample Title 2", text="Sample Text 2")
            session.add(note1)
            session.add(note2)
            session.commit()

            yield session

        finally:
            Base.metadata.drop_all(engine)


def test_delete_existing_note(setup_database):
    """
    Test deleting an existing note.
    """
    controller = NotesController()

    with Session() as session:
        note_to_delete = session.query(Note).first()
        assert note_to_delete is not None

    controller.delete(id=note_to_delete.id)

    with Session() as session:
        deleted_note = session.query(Note).filter_by(id=note_to_delete.id).first()
        assert deleted_note is None


def test_delete_nonexistent_note(setup_database):
    """
    Test attempting to delete a nonexistent note.
    """
    controller = NotesController()

    with pytest.raises(Exception, match="Note not found"):
        controller.delete(id=999)
