__all__ = ['builder']

from spytula.builder import SpytulaBuilder

builder = SpytulaBuilder()

ingredients = [
    {'name': 'Noodles', 'type': 'Main'},
    {'name': 'Pork', 'type': 'Protein'},
    {'name': 'Eggs', 'type': 'Topping'},
    {'name': 'Miso', 'type': 'Flavoring'},
]

with builder.nodes('ingredients') as add_ingredient:
    for ingredient in ingredients:
        with add_ingredient() as ingredient_builder:
            ingredient_builder.attribute('name', ingredient['name'])
            ingredient_builder.attribute('type', ingredient['type'].upper())
            
print(builder.to_json(indent=2))