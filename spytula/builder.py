import json
import yaml

from contextlib import contextmanager
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Tuple, Union

from .mixins.format import DataFormattingMixin


class SpytulaBuilder(DataFormattingMixin):
    def __init__(self, root: str = None) -> None:
        """
        Initialize a new SpytulaBuilder instance.

        Args:
            root (str): The root key for the output JSON.
        """
        super().__init__()
        self._data: Dict[str, Any] = OrderedDict()
        self._root = root

    def __enter__(self) -> 'SpytulaBuilder':
        """
        Enter the context of the SpytulaBuilder instance.
        """
        return self

    def __exit__(self, type, value, traceback) -> None:
        """
        Exit the context of the SpytulaBuilder instance.
        """
        pass

    def _new_node(self) -> 'SpytulaBuilder':
        """
        Helper method to create a new SpytulaBuilder instance.

        Returns:
            SpytulaBuilder: New instance of SpytulaBuilder.
        """
        return type(self)()

    def root(self, key: str) -> None:
        """
        Set the root key for the output JSON.

        Args:
            key (str): The root key for the output JSON.

        Example:
            ```python
            builder = SpytulaBuilder()
            builder.root("ramen")
            ```
        """
        self._root = key

    @property
    def data(self) -> Any:
        if self._root:
            return self._data[self._root]
        else:
            return self._data

    @contextmanager
    def node(self, key: str) -> 'SpytulaBuilder':
        """
        Create a new node to be added to the JSON.

        Args:
            key (str): The key for the new node in the JSON.

        Example:
            ```python
            with builder.node("ingredients") as ingredient_builder:
                ingredient_builder.attribute("name", "Ramen Noodles")
            ```
        """
        new_node = self._new_node()
        yield new_node
        self._data[key] = new_node._data

    @contextmanager
    def add_node(self, node_list: List[Dict[str, Any]]) -> 'SpytulaBuilder':
        """
        Add a new node to the given list.

        Args:
            node_list (List[Dict[str, Any]]): The list to which the node will be added.

        Example:
            ```python
            with builder.add_node(ingredient_list) as ingredient_builder:
                ingredient_builder.attribute("name", "Ramen Noodles")
            ```
        """
        new_node = self._new_node()
        yield new_node
        node_list.append(new_node._data)

    @contextmanager
    def nodes(self, key: str) -> Callable[['SpytulaBuilder'], None]:
        """
        Create a new list of nodes to be added to the JSON.

        Args:
            key (str): The key for the new list in the JSON.

        Example:
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
        """
        new_nodes: List[Dict[str, Any]] = []
        self._data[key] = new_nodes
        yield lambda: self.add_node(new_nodes)

    def each(self, key: str, items: List[Dict[str, Any]]) -> List[Tuple['SpytulaBuilder', Dict[str, Any]]]:
        """
        Iterate over a list of items and create a nested context for each item.

        Args:
            key (str): The key for the new list in the JSON.
            items (List[Dict[str, Any]]): The list of items to iterate over.

        Returns:
            List[Tuple[SpytulaBuilder, Dict[str, Any]]]: A list of tuples containing the SpytulaBuilder instance and the current item.

        Example:
            ```python
            ingredients = [
                {'name': 'Noodles', 'type': 'Main'},
                {'name': 'Pork', 'type': 'Protein'},
                {'name': 'Eggs', 'type': 'Topping'},
                {'name': 'Miso', 'type': 'Flavoring'},
            ]

            for ingredient_builder, ingredient in builder.each('ingredients', ingredients):
                ingredient_builder.attribute('name', ingredient['name'])
                ingredient_builder.attribute('type', ingredient['type'])
            ```
        """
        item_builders = []
        for item in items:
            new_item_builder = self._new_node()
            item_builders.append((new_item_builder, item))
            self._data[key] = [item_builder._data for item_builder, _ in item_builders]
        return item_builders

    def attribute(self, key: str, value: Any) -> None:
        """
        Add a new attribute to the JSON.

        Args:
            key (str): The key for the new attribute in the JSON.
            value (Any): The value of the new attribute.

        Example:
            ```python
            builder.attribute("name", "Ramen Noodles")
            ```
        """
        self._data[key] = value

    def attributes(self, obj: Any, keys: List[str]) -> None:
        """
        Add multiple new attributes to the JSON.

        Args:
            obj (Any): The object from which the attributes' values will be retrieved.
            keys (List[str]): A list of the keys for the new attributes in the JSON.

        Example:
            ```python
            ramen = {'name': 'Tonkotsu Ramen', 'type': 'Pork-based'}
            builder.attributes(ramen, ['name', 'type'])
            ```
        """
        for key in keys:
            try:
                self.attribute(key, getattr(obj, key))
            except AttributeError:
                self.attribute(key, obj[key])

    def merge(self, data: Dict[str, Any]) -> None:
        """
        Merge given dictionary into the JSON data.

        Args:
            data (Dict[str, Any]): Dictionary to merge.

        Example:
            ```python
            extra_info = {'rating': 4.5, 'spiciness': 'Medium'}
            builder.merge(extra_info)
            ```
        """
        if isinstance(data, dict):
            self._data.update(data)
        else:
            raise TypeError("Expected a dictionary to merge.")

    def when(self, key: str, value: Any, condition: Union[bool, Callable[[Any], bool]]) -> None:
        """
        Add a new attribute to the JSON when the condition is met.

        Args:
            key (str): The key for the new attribute in the JSON.
            value: The value of the new attribute.
            condition (bool or callable): Condition to be met. Can be a boolean or a lambda function that takes a value
                                          and returns a boolean.

        Example:
            ```python
            builder.when('has_noodles', True, True)
            ```
        """
        if isinstance(condition, bool):
            if condition:
                self.attribute(key, value)
        elif callable(condition):
            if condition(value):
                self.attribute(key, value)
        else:
            raise TypeError("Condition must be a boolean or a callable.")

    def partial(self, other_builder: 'SpytulaBuilder') -> None:
        """
        Merge given SpytulaBuilder instance into the current instance.

        Args:
            other_builder (SpytulaBuilder): SpytulaBuilder instance to merge.

        Example:
            ```python
            other_builder = SpytulaBuilder()
            other_builder.attribute('type', 'Ramen')
            builder.partial(other_builder)
            ```
        """
        self._data.update(other_builder._data)

    def to_json(self, *args, **kwargs) -> str:
        """
        Convert the data to a JSON-formatted string.

        Args:
            *args: Additional positional arguments to pass to json.dumps.
            **kwargs: Additional keyword arguments to pass to json.dumps.

        Returns:
            str: A JSON-formatted string representing the data.

        Example:
            ```python
            json_data = builder.to_json(indent=2)
            print(json_data)
            ```
        """
        formatted_data = self._format_data(self.data)
        return json.dumps(formatted_data, *args, **kwargs)

    def to_yaml(self, *args, **kwargs) -> str:
        """
        Convert the data to a YAML-formatted string.

        Args:
            *args: Additional positional arguments to pass to yaml.dump.
            **kwargs: Additional keyword arguments to pass to yaml.dump.

        Returns:
            str: A YAML-formatted string representing the data.

        Example:
            ```python
            yaml_data = builder.to_yaml()
            print(yaml_data)
            ```
        """
        class OrderedLoader(yaml.SafeDumper):
            pass

        def _dict_representer(dumper, data):
            resolver = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
            return dumper.represent_mapping(resolver, data.items())

        OrderedLoader.add_representer(OrderedDict, _dict_representer)

        formatted_data = self._format_data(self.data)
        return yaml.dump(formatted_data, None, OrderedLoader, *args, **kwargs)
