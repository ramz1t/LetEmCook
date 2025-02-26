import pytest
from app.models import Base, engine, Session, Note
from app.controllers.NotesController import NotesController


@pytest.fixture(scope="function")
def setup_database():
    """
    Setup a clean database for each test, creating test data and returning it.
    Yields the test database session.
    """
    # Create the database tables
    Base.metadata.create_all(engine)

    # Open a session and insert sample data
    with Session() as session:
        try:
            # Add test data for Notes
            note1 = Note(title="Sample Title 1", text="Sample Text 1")
            note2 = Note(title="Sample Title 2", text="Sample Text 2")
            session.add(note1)
            session.add(note2)
            session.commit()

            yield session  # Yield control back to tests

        finally:
            # Clean up database after test
            Base.metadata.drop_all(engine)


def test_delete_existing_note(setup_database):
    """
    Test deleting an existing note.
    """
    # Test setup
    controller = NotesController()

    # Retrieve the original note in one session
    with Session() as session:
        note_to_delete = session.query(Note).first()
        assert note_to_delete is not None  # Ensure the note exists before deletion

    # Perform the delete
    controller.delete(id=note_to_delete.id)

    # Verify the note is deleted by checking that it no longer exists
    with Session() as session:
        deleted_note = session.query(Note).filter_by(id=note_to_delete.id).first()
        assert deleted_note is None  # Note should no longer exist


def test_delete_nonexistent_note(setup_database):
    """
    Test attempting to delete a nonexistent note.
    """
    # Test setup
    controller = NotesController()

    # Attempt to delete a nonexistent note (e.g., with ID 999)
    with pytest.raises(Exception, match="Note not found"):
        controller.delete(id=999)
