import pytest
from unittest.mock import MagicMock, patch
from app.controllers.NotesController import NotesController
from app.models import Note


@patch("app.controllers.NotesController.session_scope")
def test_create_note_success(mock_session_scope):
    mock_session = MagicMock()
    mock_session_scope.return_value.__enter__.return_value = mock_session

    note_data = {
        "title": "Test Note",
        "text": "This is a test note."
    }

    mock_note = MagicMock(spec=Note)
    mock_note.to_dict.return_value = {"id": 1, "title": "Test Note", "text": "This is a test note."}

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session_scope.return_value.__enter__.return_value.add.return_value = None

    with patch("app.controllers.NotesController.Note", return_value=mock_note):
        controller = NotesController()

        result = controller.create(**note_data)

        mock_session.add.assert_called_once_with(mock_note)
        mock_session.commit.assert_called_once()
        assert result == {"id": 1, "title": "Test Note", "text": "This is a test note."}


@patch("app.controllers.NotesController.session_scope")
def test_create_note_rejects_blank_title(mock_session_scope):

    mock_session = MagicMock()
    mock_session_scope.return_value.__enter__.return_value = mock_session

    note_data = {
        "title": "",
        "text": "This is a test note."
    }

    controller = NotesController()

    with pytest.raises(Exception, match="Something went wrong: Error: title or text missing"):
        controller.create(**note_data)
