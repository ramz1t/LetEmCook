from app.models import session_scope, Note

class NotesController:
    def create(self, **kwargs) -> dict:
            with session_scope() as session:
                note = Note(**kwargs)
                session.add(note)
                session.commit()
                return note.to_dict()

    def list(self, search: str = str()):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, id: int):
        pass