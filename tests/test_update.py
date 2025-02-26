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
            note1 = Note(title="Old Title", text="Old Text")
            session.add(note1)
            session.commit()

            yield session  # Yield control back to tests

        finally:
            # Clean up database after test
            Base.metadata.drop_all(engine)


def test_update_existing_note(setup_database):
    """
    Test updating an existing note.
    """
    # Test setup
    controller = NotesController()

    # Updated data
    updated_data = {"title": "New Title", "text": "Updated Text"}

    # Retrieve the original note in one session
    with Session() as session:
        original_note = session.query(Note).first()
        assert original_note is not None  # Validate note exists before update

    # Perform the update
    result = controller.update(id=original_note.id, **updated_data)

    # Re-fetch the note in a new session after the update
    with Session() as session:
        updated_note = session.query(Note).filter_by(id=original_note.id).first()

        # Verify the updates
        assert updated_note.title == "New Title"
        assert updated_note.text == "Updated Text"
        assert result["title"] == "New Title"
        assert result["text"] == "Updated Text"


def test_update_nonexistent_note(setup_database):
    """
    Test updating a note that does not exist.
    """
    # Test setup
    controller = NotesController()

    with pytest.raises(Exception, match="Note not found"):
        controller.update(id=999, title="Nonexistent")


def test_update_partial_fields(setup_database):
    """
    Test updating a note with partial fields (e.g., only title).
    """
    # Test setup
    controller = NotesController()

    # Partial update data
    partial_data = {"title": "New Title"}

    # Retrieve the original note in one session
    with Session() as session:
        original_note = session.query(Note).first()
        assert original_note is not None  # Validate note exists before update

    # Perform the update
    result = controller.update(id=original_note.id, **partial_data)

    # Re-fetch the note in a new session after the update
    with Session() as session:
        updated_note = session.query(Note).filter_by(id=original_note.id).first()

        # Verify only the title was updated, while the text remains unchanged
        assert updated_note.title == "New Title"
        assert updated_note.text == "Old Text"  # Text should remain unchanged
        assert result["title"] == "New Title"
        assert result["text"] == "Old Text"  # Ensure text remains unchanged
