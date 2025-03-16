import pytest
from app.models import Base, engine, Session, Note
from app.controllers.NotesController import NotesController



@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(engine)

    with Session() as session:
        try:
            note1 = Note(title="Tasty Pizza", text="A delicious cheese and pepperoni pizza recipe.")
            note2 = Note(title="Healthy Salad", text="A step-by-step guide to making a Caesar salad.")
            note3 = Note(title="Other Recipe", text="Some instructions about cooking rice.")
            session.add(note1)
            session.add(note2)
            session.add(note3)
            session.commit()

            yield session

        finally:
            Base.metadata.drop_all(engine)


def test_list_all_notes(setup_database):
    controller = NotesController()

    result = controller.list(search="")

    assert len(result) == 3
    assert any(note['title'] == "Tasty Pizza" for note in result)
    assert any(note['title'] == "Healthy Salad" for note in result)
    assert any(note['title'] == "Other Recipe" for note in result)


def test_list_notes_with_search(setup_database):
    controller = NotesController()

    result = controller.list(search="Pizza")

    assert len(result) == 1
    assert result[0]['title'] == "Tasty Pizza"
    assert "pizza recipe" in result[0]['text'].lower()


def test_list_notes_with_partial_match(setup_database):
    controller = NotesController()

    result = controller.list(search="Salad")

    assert len(result) == 1
    assert result[0]['title'] == "Healthy Salad"
    assert "Caesar salad" in result[0]['text']


def test_list_notes_no_match(setup_database):
    controller = NotesController()

    result = controller.list(search="Burger")

    assert len(result) == 0
