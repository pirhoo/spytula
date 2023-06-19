import inflection
import inspect

from collections import OrderedDict
from collections.abc import Iterable
from typing import Any, Dict


class KeyFormatMixin:
    def __init__(self) -> None:
        self._key_format = None

    @property
    def _inflection_methods(self):
        return [
            name
            for name, _ in inspect.getmembers(inflection, inspect.isfunction)
            if isinstance(name, str) and name[0].isalpha()
        ]

    def key_format(self, **kwargs) -> None:
        """
        Configure the key formatting options.

        Args:
            **kwargs: Key formatting options.

        Raises:
            ValueError: If an unsupported formatting option is provided.
        """
        unsupported_options = set(kwargs.keys()) - set(self._inflection_methods)
        if unsupported_options:
            raise ValueError(f"Unsupported key formatting options: {', '.join(unsupported_options)}")
        self._key_format = kwargs

    def _format_key(self, key: str) -> str:
        """
        Format the key based on the configured key formatting options.

        Args:
            key (str): The key to format.

        Returns:
            str: Formatted key.
        """
        if self._key_format:
            for format_option, format_args in self._key_format.items():
                key_formatter = getattr(inflection, format_option, None)
                if key_formatter is not None:
                    if type(format_args) is dict:
                        key = key_formatter(key, **format_args)
                    elif isinstance(format_args, Iterable):
                        key = key_formatter(key, *format_args)
                    elif format_args == True:
                        key = key_formatter(key)
        return key


class DataFormattingMixin(KeyFormatMixin):
    def _format_data(self, data: Any) -> Dict[str, Any]:
        """
        Recursively format the keys in the data based on the configured key formatting options.

        Args:
            data (Dict[str, Any]): The data to format.

        Returns:
            Dict[str, Any]: Formatted data.
        """
        if isinstance(data, dict):
            formatted_data = OrderedDict()
            for key, value in data.items():
                formatted_key = self._format_key(key)
                if isinstance(value, dict):
                    formatted_value = self._format_data(value)
                else:
                    formatted_value = value
                formatted_data[formatted_key] = formatted_value
            return formatted_data
        elif isinstance(data, list):
            return [ self._format_data(value) for value in data ]
        else:
            return data