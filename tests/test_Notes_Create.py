import pytest
from unittest.mock import MagicMock, patch
from app.controllers.NotesController import NotesController
from app.models import Note


# Example test class
class TestNotesController:
    @patch("app.controllers.NotesController.session_scope")  # Mock the session_scope
    def test_create_note_success(self, mock_session_scope):
        # Set up the mock session
        mock_session = MagicMock()
        mock_session_scope.return_value.__enter__.return_value = mock_session

        # Prepare input data
        note_data = {
            "title": "Test Note",
            "text": "This is a test note."
        }

        # Mock the behavior of Note to_dict()
        mock_note = MagicMock(spec=Note)
        mock_note.to_dict.return_value = {"id": 1, "title": "Test Note", "text": "This is a test note."}

        # Mock the creation and database interaction
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session_scope.return_value.__enter__.return_value.add.return_value = None

        # Simulate Note(**kwargs)
        with patch("app.controllers.NotesController.Note", return_value=mock_note):
            controller = NotesController()

            # Call the function
            result = controller.create(**note_data)

            # Verify the behavior
            mock_session.add.assert_called_once_with(mock_note)
            mock_session.commit.assert_called_once()
            assert result == {"id": 1, "title": "Test Note", "text": "This is a test note."}

