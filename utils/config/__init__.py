"""
Utilities for managing configuration.

This module provides a `Configuration` class for managing configuration files
and mapping values from the configuration to their actual values.

The `Configuration` class uses a dictionary to map configuration keys to their
actual values. The keys in this dictionary are the keys in the configuration
file, and the values are functions that take the value from the configuration
file and return the actual value.

The `Configuration` class provides a `__getitem__` method to allow for
direct access to the configuration values using the key as a string. If the
key does not exist, a `KeyError` is raised.

"""

from utils.config.config import Configuration as BaseConfiguration
from utils.config.mapping import MAPPING, ITERABLES_MAPPING


class Configuration(BaseConfiguration):
    def __init__(self, config_path: str | None = None):
        super().__init__(MAPPING, ITERABLES_MAPPING, config_path)

__all__ = ['Configuration']
