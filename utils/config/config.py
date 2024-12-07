'''Tools to manage config file'''

import json
import os
import re
import warnings
from itertools import cycle
from typing import Any, Dict

PREMADE_CONFIGS = {}

for filename in os.listdir('configs'):
    if filename.endswith('.json'):
        with open(f'configs/{filename}', encoding='utf-8') as f:
            PREMADE_CONFIGS[filename[:-5]] = json.load(f)

class Configuration:
    def __init__(self, mapping: dict, iterables_mapping: dict, config_path: str | None, secrets_path: str | None) -> None:
       
        
        self._config = {}

        if config_path:
            with open(config_path, encoding='utf-8') as f:
                self._config = json.load(f)

        for key in self._config.keys():
            if key.startswith('_'):
                warnings.warn('Trying to set a protected key: ' + key)
        
        # Get the name of the base configuration
        default_config_name = self._config.get('config', 'default')

        # Get the base configuration
        base_config = PREMADE_CONFIGS[default_config_name]
        if default_config_name != 'default':
            for key in base_config.keys():
                if key.startswith('_'):
                    warnings.warn('Trying to set a protected key: ' + key)

        # Update the base configuration with the default values from even more default configuration if they are not present
        # This is to ensure that all the default values are present in the base configuration
        base_config.update({key: value for key, value in PREMADE_CONFIGS['default'].items() if key not in base_config})

        # Update the configuration with the values from the base configuration if they are not present
        # This is to ensure that all the keys are present in the configuration
        self._config.update({key: value for key, value in base_config.items() if key not in self._config})

        try:
            with open('secrets.json', encoding='utf-8') as file:
                secrets = json.load(file)
        except FileNotFoundError:
            secrets = {}
        for key, value in secrets.items():
            secrets[key] = cycle(value)
        
        iterables_mapping.update(secrets)
                   
        self._mapping = mapping
        self._iterables_mapping = iterables_mapping
    
    def retrieve_map(self, value):
        """
        Retrieves a value from either the mapping or the iterable mapping.
        
        If the value is not found in either the mapping or the iterable mapping,
        a TypeError is raised. If the value is a dictionary, it is recursively
        mapped. If the value is a list, it is iteratively mapped.
        
        Parameters
        ----------
        value : object
            The value to be retrieved
        
        Returns
        -------
        object
            The retrieved value
        
        Raises
        ------
        KeyError
            If the value is not found in either the mapping or the iterable mapping
        TypeError
            If the value is not a dictionary or a list
        """
        try:
            if value in self._iterables_mapping:
                return next(self._iterables_mapping[value])
            elif value in self._mapping:
                return self._mapping[value]
            else:
                raise TypeError
        except TypeError:
            
            if isinstance(value, dict):
                mapped = {k: self.map(v) for k, v in value.items()}
                if set(mapped.keys()) == {'type', 'args', 'kwargs'}:
                    return self.map(mapped['type'])(*mapped['args'], **mapped['kwargs'])
                return mapped
            elif isinstance(value, list):
                return [self.map(v) for v in value]
            raise KeyError(str(value))

    def map(self, value):
        """
        Maps a value to its corresponding value in either the mapping or the iterable mapping.
        
        If the value is not found in either the mapping or the iterable mapping,
        the value itself is returned.
        
        Parameters
        ----------
        value : object
            The value to be mapped
        
        Returns
        -------
        object
            The mapped value
        """
        try:
            return self.retrieve_map(value)
        except KeyError:
            return value
    
    def __getitem__(self, key) -> Any:
        
        if key in self._config:
            return self.map(self._config[key])
        elif key.endswith('_model'):
            try:
                model_type = key + '_type'
                model_args = key + '_args'
                model_kwargs = key + '_kwargs'
                model = self[model_type](*self[model_args], **self[model_kwargs])
                self._config[key] = model
                return model
            except KeyError:
                raise KeyError(str(key))
        elif key.endswith('_args'):
            return []
        elif key.endswith('_kwargs'):
            return {}
        else:
            # check if the key is a path
            for sep in ('/', '\\\\'):
                if re.search(sep, key):
                    folders = key.split(sep)
                    path = ''
                    for i, folder in enumerate(folders):
                        if folder.startswith('!'):
                            real_folder = folder[1:]
                            if real_folder == '__new__':
                                os.makedirs(path, exist_ok=True)
                                i = 0
                                while os.path.exists(os.path.join(path, str(i))):
                                    i += 1
                                real_folder = str(i)
                                os.mkdir(os.path.join(path, real_folder))
                        else:
                            try:
                                real_folder = self._config[folder]
                            except KeyError:
                                real_folder = folder
                        if i == len(folders)-1:
                            filename = folder
                            real_filename = real_folder
                            name, ext = os.path.splitext(filename)
                            _, real_ext = os.path.splitext(real_filename)
                            if not ext:
                                ext = real_ext
                            real_folder = name+ext
                        path = os.path.join(path, real_folder)
                    return path
            
            # check if key is something to map, otherwise raise KeyError
            
            return self.retrieve_map(key)
        
    