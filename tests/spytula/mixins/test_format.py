import pytest
import json

from spytula.builder import SpytulaBuilder

@pytest.fixture
def builder():
    return SpytulaBuilder()

def test_key_format_camelcase(builder):
    # Given
    builder.attribute('pizza_name', 'Margherita')
    builder.key_format(camelize={'uppercase_first_letter': False})
    # When
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert 'pizzaName' in data

def test_key_format_underscore(builder):
    # Given
    builder.attribute('crustType', 'Thin')
    builder.key_format(underscore=True)
    # When
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert 'crust_type' in data

def test_key_format_multiple_options(builder):
    # Given
    builder.attribute('order_number', 123)
    builder.key_format(dasherize=True, camelize={'uppercase_first_letter': True})
    # When
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then    
    assert 'Order-number' in data

def test_key_format_unsupported_option(builder):
    with pytest.raises(ValueError):
        builder.key_format(capitalize=True)

def test_key_format_no_options(builder):
    # Given
    builder.attribute('pizza_name', 'Margherita')
    builder.key_format()
    # When
    json_output = builder.to_json()
    data = json.loads(json_output)
    # Then
    assert 'pizza_name' in data
