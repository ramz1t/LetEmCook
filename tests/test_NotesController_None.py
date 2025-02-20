import pytest
from unittest.mock import patch, MagicMock
from app.controllers.NotesController import NotesController


@patch("app.controllers.NotesController.session_scope")  # Mock the session_scope
def test_create_note_rejects_blank_title(mock_session_scope):
    # Set up the mock session
    mock_session = MagicMock()
    mock_session_scope.return_value.__enter__.return_value = mock_session

    # Prepare input data with a blank title
    note_data = {
        "title": "",
        "text": "This is a test note."
    }

    controller = NotesController()

    # Call the function and assert it raises the `Exception` due to the controller wrapping
    with pytest.raises(Exception, match="Something went wrong: Error: title or text missing"):
        controller.create(**note_data)
