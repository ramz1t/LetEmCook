import pytest
from app.models import Base, engine, Session, Note
from app.controllers.NotesController import NotesController


@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(engine)

    with Session() as session:
        try:
            note1 = Note(title="Old Title", text="Old Text")
            session.add(note1)
            session.commit()

            yield session

        finally:
            Base.metadata.drop_all(engine)


def test_update_existing_note(setup_database):
    controller = NotesController()

    updated_data = {"title": "New Title", "text": "Updated Text"}

    with Session() as session:
        original_note = session.query(Note).first()
        assert original_note is not None

    result = controller.update(id=original_note.id, **updated_data)

    with Session() as session:
        updated_note = session.query(Note).filter_by(id=original_note.id).first()

        assert updated_note.title == "New Title"
        assert updated_note.text == "Updated Text"
        assert result["title"] == "New Title"
        assert result["text"] == "Updated Text"


def test_update_nonexistent_note(setup_database):
    controller = NotesController()

    with pytest.raises(Exception, match="Note not found"):
        controller.update(id=999, title="Nonexistent")


def test_update_partial_fields(setup_database):
    controller = NotesController()

    partial_data = {"title": "New Title"}

    with Session() as session:
        original_note = session.query(Note).first()
        assert original_note is not None

    result = controller.update(id=original_note.id, **partial_data)

    with Session() as session:
        updated_note = session.query(Note).filter_by(id=original_note.id).first()


        assert updated_note.title == "New Title"
        assert updated_note.text == "Old Text"
        assert result["title"] == "New Title"
        assert result["text"] == "Old Text"