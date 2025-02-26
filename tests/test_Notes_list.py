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

    # Open a session and insert sample food-related data
    with Session() as session:
        try:
            # Add test data for Notes
            note1 = Note(title="Tasty Pizza", text="A delicious cheese and pepperoni pizza recipe.")
            note2 = Note(title="Healthy Salad", text="A step-by-step guide to making a Caesar salad.")
            note3 = Note(title="Other Recipe", text="Some instructions about cooking rice.")
            session.add(note1)
            session.add(note2)
            session.add(note3)
            session.commit()

            yield session  # Yield control back to tests

        finally:
            # Clean up database after test
            Base.metadata.drop_all(engine)


def test_list_all_notes(setup_database):
    """
    Test the list function with no search query (should return all notes).
    """
    # Test setup
    controller = NotesController()

    # Perform the list operation with an empty search query
    result = controller.list(search="")

    # Verify that all notes are returned
    assert len(result) == 3  # Matches the number of inserted notes
    assert any(note['title'] == "Tasty Pizza" for note in result)
    assert any(note['title'] == "Healthy Salad" for note in result)
    assert any(note['title'] == "Other Recipe" for note in result)


def test_list_notes_with_search(setup_database):
    """
    Test the list function with a search query (should return matching notes).
    """
    # Test setup
    controller = NotesController()

    # Perform the list operation with a search term
    result = controller.list(search="Pizza")

    # Verify that only notes containing the search term are returned
    assert len(result) == 1  # One note contains "Pizza" in its title
    assert result[0]['title'] == "Tasty Pizza"
    assert "pizza recipe" in result[0]['text'].lower()


def test_list_notes_with_partial_match(setup_database):
    """
    Test the list function with a search query that partially matches note content.
    """
    # Test setup
    controller = NotesController()

    # Perform the list operation with a partial search term
    result = controller.list(search="Salad")

    # Verify that the correct note is returned
    assert len(result) == 1  # One note contains "Salad" in its title
    assert result[0]['title'] == "Healthy Salad"
    assert "Caesar salad" in result[0]['text']


def test_list_notes_no_match(setup_database):
    """
    Test the list function with a search query that doesn’t match any notes.
    """
    # Test setup
    controller = NotesController()

    # Perform the list operation with a term not present in any note
    result = controller.list(search="Burger")

    # Verify the result is empty
    assert len(result) == 0  # No note matches the query
