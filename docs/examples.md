## Adding an attribute

To add attributes to the JSON or YAML data, use the `attribute` method:

```python
builder.attribute('name', 'Ramen')
builder.attribute('origin', 'Japan')
```

Which gives the following JSON output:

```json
{
  "name": "Ramen",
  "origin": "Japan"
}
```

## Adding several attributes

To add attributes to the JSON or YAML data, use the `attributes` method:

```python
dish = {
  'name': 'Ramen',
  'type': 'Japan',
  'rating': 4.5
}

builder.attributes(dish, ['name', 'origin'])
```

Which gives the following JSON output:

```json
{
  "name": "Ramen",
  "origin": "Japan"
}
```

## Creating single node

A single node can be created using the `node` method, which allows building nested structures:

```python
with builder.node('dish') as dish:
    dish.attribute('name', 'Ramen')
    dish.attribute('origin', 'Japan')
    dish.attribute('rating', 4.5)
```

Which gives the following JSON output:

```json
{
  "dish": {
    "name": "Ramen",
    "origin": "Japan",
    "rating": 4.5
  }
}

```

## Creating lists of nodes

Lists of nodes can be created using the `nodes` method:

```python
with builder.nodes('ingredients') as add_ingredient:
    with add_ingredient() as ingredient1:
        ingredient1.attribute('name', 'Noodles')
        ingredient1.attribute('type', 'Main')
    
    with add_ingredient() as ingredient2:
        ingredient2.attribute('name', 'Pork')
        ingredient2.attribute('type', 'Protein')
    
    with add_ingredient() as ingredient3:
        ingredient3.attribute('name', 'Eggs')
        ingredient3.attribute('type', 'Additional')
```

This is perfect when dealing with a collections:

```python
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
```

Which gives the following JSON output:

```json
{
  "ingredients": [
    {
      "name": "Noodles",
      "type": "MAIN"
    },
    {
      "name": "Pork",
      "type": "PROTEIN"
    },
    {
      "name": "Eggs",
      "type": "TOPPING"
    },
    {
      "name": "Miso",
      "type": "FLAVORING"
    }
  ]
}
```

You can also use the short-hand `each` method:

```python
ingredients = [
    {'name': 'Noodles', 'type': 'Main'},
    {'name': 'Pork', 'type': 'Protein'},
    {'name': 'Eggs', 'type': 'Topping'},
    {'name': 'Miso', 'type': 'Flavoring'},
]

for (ingredient_builder, ingredient) in builder.each('ingredients', ingredients):
    ingredient_builder.attribute('name', ingredient['name'])
    ingredient_builder.attribute('type', ingredient['type'].upper())
```

## Merging data

You can merge data into the JSON using the `merge` method:

```python
data = {'rating': 4.5, 'serving': 'Bowl'}
builder.merge(data)
```

## Conditional attributes

You can add attributes conditionally using the `when` method:

```python
builder.when('spicy', True, 'Chili' in ingredients)
```

## Converting to json

To convert the builder to a JSON-formatted string, use the `to_json` method:

```python
json_output = builder.to_json(ident=2)
print(json_output)
```

## Converting to yaml

To convert the builder to a YAML-formatted string, use the `to_yaml` method:

```python
yaml_output = builder.to_yaml()
print(yaml_output)
```
