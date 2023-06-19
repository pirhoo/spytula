# Spytula

Spytula is a Python library that provides a simple and convenient way to build JSON and YAML data structures using a builder pattern.

## Installation

Use pip to install the Spytula library:

```bash
pip install spytula
```

## Usage    

Import the `SpytulaBuilder` class from the `spytula.builder` module:

```python
from spytula.builder import SpytulaBuilder

# Create an instance of SpytulaBuilder
builder = SpytulaBuilder()

# Add attributes to the JSON structure
builder.attribute('name', 'Ramen')
builder.attribute('origin', 'Japan')

# Create a list of ingredients
for builder.each('ingredients') as add_ingredient:    
    for ingredient in ['Noodles', 'Pork', 'Eggs', 'Miso']:
        with add_ingredient() as ingredient_builder:
            ingredient_builder.attribute('name', ingredient)

# Add optional attributes conditionally
builder.when('spiciness', 'Medium', True)
builder.when('extra_toppings', ['Green Onions', 'Nori', 'Bamboo Shoots'], True)

# Configure the key to use camelcase
builder.key_format(camelize={'uppercase_first_letter': False})

# Convert the JSON structure to JSON-formatted string
json_output = builder.to_json(indent=4)

# Print the JSON output
print(json_output)
```

This will output:

```json
{
    "name": "Ramen",
    "origin": "Japan",
    "ingredients": [
        { "name": "Noodles" },
        { "name": "Pork" },
        { "name": "Eggs" },
        { "name": "Miso" }
    ],
    "spiciness": "Medium",
    "extraToppings": [
        "Green Onions",
        "Nori",
        "Bamboo Shoots"
    ]
}

```

In this example, we create a `SpytulaBuilder` instance and add attributes like name and origin to represent `Ramen`. We use the `nodes()` context manager to create a list of ingredients and add them to the JSON structure. Optional attributes like spiciness and toppings are added conditionally using the `when()` method. Finally, we convert the JSON structure to a JSON-formatted string using `to_json()` with an indentation of 4 spaces.
