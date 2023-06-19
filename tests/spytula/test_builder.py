import pytest
import json
import yaml
from spytula.builder import SpytulaBuilder

@pytest.fixture
def dish():
    return {
        'name': 'Ramen',
        'origin': 'Japan',
        'ingredients': ['Noodles', 'Pork', 'Eggs', 'Miso'],
    }

@pytest.fixture()
def builder():
    return SpytulaBuilder()

@pytest.fixture()
def list_builder():
    return SpytulaBuilder()

def test_spytula_builder_name(builder, dish):
    # When
    builder.attribute('name', dish['name'])
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert data['name'] == 'Ramen'

def test_spytula_builder_origin(builder, dish):
    # When
    builder.attribute('origin', dish['origin'])
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert data['origin'] == 'Japan'

def test_spytula_builder_merge(builder):
    # Given
    data = {'author': {'name': "David"}}
    # When
    with builder.node('post') as post:
        post.attribute('title', "Merge HOWTO")
        post.merge(data)
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert data['post']['title'] == "Merge HOWTO"
    assert data['post']['author']['name'] == "David"

def test_spytula_builder_ingredients(builder, dish):
    # When
    with builder.nodes('ingredients') as add_ingredient:
        for ingredient in dish['ingredients']:
            with add_ingredient() as ingredient_builder:
                ingredient_builder.attribute('name', ingredient)
    json_output = builder.to_json()
    data = json.loads(json_output)
    ingredient_names = [item['name'] for item in data['ingredients']]
    # Then
    assert 'Noodles' in ingredient_names

def test_spytula_builder_each(builder):
    # Given
    ingredients = [
        {'name': 'Noodles', 'type': 'Main'},
        {'name': 'Pork', 'type': 'Protein'},
        {'name': 'Eggs', 'type': 'Topping'},
        {'name': 'Miso', 'type': 'Flavoring'},
    ]

    # When
    for (ingredient_builder, ingredient) in builder.each('ingredients', ingredients):
        ingredient_builder.attribute('name', ingredient['name'])
        ingredient_builder.attribute('type', ingredient['type'])

    json_output = builder.to_json(indent=4)
    data = json.loads(json_output)
    # Then
    assert len(data['ingredients']) == len(ingredients)
    for idx, ingredient in enumerate(data['ingredients']):
        assert ingredient['name'] == ingredients[idx]['name']
        assert ingredient['type'] == ingredients[idx]['type']

def test_spytula_builder_multiple_attributes(builder, dish):
    # When
    builder.attributes(dish, ['name', 'origin'])
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert data['name'] == 'Ramen'
    assert data['origin'] == 'Japan'

def test_spytula_builder_ingredients_with_no_name(builder, dish):
    # When
    with builder.nodes('ingredients') as add_ingredient:
        for _ in dish['ingredients']:
            with add_ingredient() as ingredient_builder:
                ingredient_builder.attribute('name', '')
    json_output = builder.to_json()
    data = json.loads(json_output)
    ingredient_names = [item['name'] for item in data['ingredients']]
    # Then
    assert '' in ingredient_names

def test_spytula_builder_ingredients_with_no_ingredients(builder, dish):
    # Given
    dish['ingredients'] = []
    # When
    with builder.nodes('ingredients') as add_ingredient:
        for ingredient in dish['ingredients']:
            with add_ingredient() as ingredient_builder:
                ingredient_builder.attribute('name', ingredient)
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert data['ingredients'] == []

def test_spytula_builder_when_boolean_condition_true(builder):
    builder.when('origin', 'Japan', True)
    json_output = builder.to_json()
    data = json.loads(json_output)
    assert data['origin'] == 'Japan'

def test_spytula_builder_when_boolean_condition_false(builder):
    builder.when('origin', 'Japan', False)
    json_output = builder.to_json()
    data = json.loads(json_output)
    assert 'origin' not in data

def test_spytula_builder_when_lambda_condition_true(builder):
    builder.when('age', 25, lambda x: x > 18)
    json_output = builder.to_json()
    data = json.loads(json_output)
    assert data['age'] == 25

def test_spytula_builder_when_lambda_condition_false(builder):
    builder.when('age', 15, lambda x: x > 18)
    json_output = builder.to_json()
    data = json.loads(json_output)
    assert 'age' not in data

def test_spytula_builder_partial(builder):
    # Given
    partial_builder = SpytulaBuilder()
    partial_builder.attribute('origin', 'Japan')
    # When
    builder.partial(partial_builder)
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert data['origin'] == 'Japan'

def test_to_json(builder):
    # Given
    builder.attribute("name", "John Doe")
    builder.attribute("age", 30)
    # When
    json_string = builder.to_json(indent=4)
    expected_json = {
        "name": "John Doe",
        "age": 30
    }
    # Then
    assert json.loads(json_string) == expected_json

def test_to_yaml(builder):
    # Given
    builder.attribute("name", "John Doe")
    builder.attribute("age", 30)
    # When
    yaml_string = builder.to_yaml(default_flow_style=False)
    expected_yaml = "age: 30\nname: John Doe"
    # Then
    assert yaml.safe_load(yaml_string) == yaml.safe_load(expected_yaml)

def test_with_root_option(builder, dish):
    # Given
    builder.root("ingredients")
    builder.merge(dish)
    # When
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert 'Noodles' in data
    assert 'Pork' in data
    assert len(data) == 4