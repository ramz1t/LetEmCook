from app.models import session_scope, Note

class NotesController:
    def create(self, **kwargs) -> dict:
        try:
            if not kwargs.get("title") or not kwargs.get("text"):
                raise ValueError("Error: title or text missing")

            with session_scope() as session:
                note = Note(**kwargs)
                session.add(note)
                session.commit()
                return note.to_dict()

        except Exception as e:
            raise Exception(f"Something went wrong: {str(e)}")

    def list(self, search: str = str()):
        try:
            with session_scope() as session:
                note_list = session.query(Note)
                if search:
                    note_list = note_list.filter(Note.title.contains(search) | Note.text.contains(search))

                notes = note_list.all()

                return [note.to_dict() for note in notes]

        except Exception as e:
            raise Exception(f"Something went wrong: {str(e)}")

    def update(self, id: int, **kwargs):
        try:
            with session_scope() as session:
                note = session.query(Note).get(id)
                if not note:
                    raise Exception("Note not found")

                for key, value in kwargs.items():
                    if hasattr(note, key):
                        setattr(note, key, value)

                return note.to_dict()

        except Exception as e:
            raise Exception(f"Something went wrong: {str(e)}")


    def delete(self, id: int):
        try:
            with session_scope() as session:
                note = session.query(Note).get(id)
                if not note:
                    raise Exception("Note not found")

                session.delete(note)

        except Exception as e:
            raise Exception(f"Something went wrong: {str(e)}")