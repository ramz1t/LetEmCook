import json

from app.models import session_scope, Ingredient

if __name__ == '__main__':
    with open('resources/ingredients.json', 'r') as file:
        data = json.load(file)

    with session_scope() as session:
        for ingredient_data in data:
            ingredient = session.query(Ingredient).filter_by(name=ingredient_data['name']).first()
            if ingredient:
                print("Skipped", ingredient_data['name'])
                continue
            session.add(Ingredient(**ingredient_data))
            print("Added", ingredient_data['name'])