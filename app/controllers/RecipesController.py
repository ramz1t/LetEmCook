from typing import List

from app.models import session_scope, Recipe


class RecipesController:

    # Create recipe

    # Get all recipes (can be filtered by name)
    def list(self, search: str = "", ) -> List[Recipe]:
        with session_scope() as session:
            if search:
                search_term = f'%{search}%'
                recipes = session.query(Recipe).filter(Recipe.name.ilike(search_term)) | session.query(Recipe).filter(Recipe.description.ilike(search_term)).all()
            else:
                recipes = session.query(Recipe).all()
            return recipes


    # Edit recipe by id and dict of changes

    # Delete recipe

    pass
