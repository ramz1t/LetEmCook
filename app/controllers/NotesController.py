from app.models import session_scope, Note

class NotesController:
    def create(self, **kwargs) -> dict:
        try:
            if not kwargs.get("title") or not kwargs.get("text"):
                return {"error": "title or text missing"}

            with session_scope() as session:
                note = Note(**kwargs)
                session.add(note)
                session.commit()
                return note.to_dict()

        except Exception as e:
            return {"Error": f"Something went wrong: {str(e)}"}

    def list(self, search: str = str()):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, id: int):
        pass