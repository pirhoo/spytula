# Spytula

Spytula is a Python library for building JSON and YAML data structures easily. It provides a fluent and intuitive API to construct complex data hierarchies.

## Installation

You can install Spytula using pip:

```bash
pip install spytula
```

## Usage

Spytula offers a simple and flexible way to build JSON and YAML data structures. Here's a quick example:

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

## Documentation

The documentation is generated from the docstrings in the code using the `mkdocstrings` plugin. It provides detailed information about the classes, methods, and attributes in the Spytula library.

You can explore the [API Documentation](api.md) for more information.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/pirhoo/spytula). If you're willing to help, check the page about [how to contribute](contributing.md) to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/pirhoo/spytula/blob/main/LICENSE.md) file for more details.
