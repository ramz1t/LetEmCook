import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, declarative_base
from contextlib import contextmanager

from config import PROJECT_PATH

Base = declarative_base()
engine = create_engine('sqlite:///' + os.path.join(PROJECT_PATH, 'app', 'data.db'))
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_scope():
    """
    Context manager for transactional database sessions.
    Ensures sessions are committed or rolled back and closed properly.

    Usage:
    with session_scope() as session:
        # Perform database operations
        session.add(new_record)

    Yields:
    session: SQLAlchemy session object

    Raises:
    Exception: Rolls back session on error
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    recipe_ingredients = relationship(
        'RecipeIngredient',
        back_populates='recipe',
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    ingredients = relationship(
        'Ingredient',
        secondary='recipe_ingredients',
        back_populates='recipes',
        overlaps='recipe_ingredients',
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ingredients': [
                {
                    'quantity': ri.quantity,
                    **ri.ingredient.to_dict()
                }
                 for ri in self.recipe_ingredients
            ]
        }


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    calories = Column(Float)
    fats = Column(Float)
    sugars = Column(Float)
    carbohydrates = Column(Float)
    protein = Column(Float)

    recipe_ingredients = relationship(
        'RecipeIngredient',
        back_populates='ingredient',
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    recipes = relationship(
        'Recipe',
        secondary='recipe_ingredients',
        back_populates='ingredients',
        overlaps='recipe_ingredients'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'calories': self.calories,
            'fats': self.fats,
            'sugars': self.sugars,
            'carbohydrates': self.carbohydrates,
            'protein': self.protein,
        }


class RecipeIngredient(Base):
    """
    Used to link recipe and ingredient with quantity needed

    Usage:
    # Create
    recipe = Recipe(name='Pancake', description='A simple pancake recipe')
    ingredient1 = Ingredient(name='Flour', unit='grams', calories=364, fats=1.2, sugars=0.3, carbohydrates=76,
                                 protein=9.1)
    ingredient2 = Ingredient(name='Sugar', unit='grams', calories=387, fats=0, sugars=99.9, carbohydrates=99.9,
                                 protein=0)
    recipe_ingredient1 = RecipeIngredient(recipe=recipe, ingredient=ingredient1, quantity=200)
    recipe_ingredient2 = RecipeIngredient(recipe=recipe, ingredient=ingredient2, quantity=50)

    # Get
    retrieved_recipe = session.query(Recipe).first()
    print(f'Recipe Name: {retrieved_recipe.name}')
    print(f'Recipe Description: {retrieved_recipe.description}')
    for ri in retrieved_recipe.recipe_ingredients:
        print(f'Ingredient Name: {ri.ingredient.name}')
        print(f'Amount: {ri.quantity}')
        print(f'Fats: {ri.ingredient.fats}')
        print(f'Sugars: {ri.ingredient.sugars}')
        print(f'Carbohydrates: {ri.ingredient.carbohydrates}')
        print(f'Protein: {ri.ingredient.protein}')
    """
    __tablename__ = 'recipe_ingredients'
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id', ondelete='CASCADE', name='fk_recipe_id_recipes'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id', ondelete='CASCADE', name='fk_ingredient_id_ingredients'))
    quantity = Column(Float)

    recipe = relationship(
        'Recipe',
        back_populates='recipe_ingredients',
    )
    ingredient = relationship(
        'Ingredient',
        back_populates='recipe_ingredients',
    )


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text
        }
