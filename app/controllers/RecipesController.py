from app.models import session_scope, Recipe


class RecipesController:

    # Create recipe

    # Get all recipes (can be filtered by name)

    # Edit recipe by id and dict of changes

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            recipe = session.query(Recipe).filter_by(id=id).first()
            if recipe:
                session.delete(recipe)
                return True
            return False
