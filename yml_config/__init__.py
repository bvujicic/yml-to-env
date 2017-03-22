import collections
import os

import yaml


class Config(collections.UserDict):
    """
    Instantiate this object with a dictionary or by parsing a YAML file with from_yaml method.
    Once instantiated use to_env to dump all the data into environment variables.
    Or use key assignment to assign specific values to environment.
    """
    def __setitem__(self, key, value):
        """
        Update both the object and the environment variable.
        """
        self.data.update({key: value})
        self.to_env(data={key: value})

    def __call__(self, value, default=None):
        return os.environ.get(value, default)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self.data))

    @classmethod
    def from_yaml(cls, path='.config.yml'):
        """
        Parses YAML config file and creates a Config instance with resulting dictionary.

        :param path: (str) YAML config path
        :return: (Config)
        """
        try:
            with open(path, 'r') as fp:
                yaml_dict = yaml.load(stream=fp)

        except IOError:
            raise IOError('YAML config file not found.')

        else:
            return cls(yaml_dict)

    def to_env(self, data=None, parent_key=''):
        """
        Exports config data as environment variables by iterating through dictionary data.
        If value is a sequence, export it as whitespace separated string.
        If value is a mapping, continue recursively.
        If value is literal, cast it as str and export directly.

        :param data: 
        :param parent_key:
        :return:
        """
        env = os.environ
        if data is None:
            data = self.data

        for key, value in data.items():

            if isinstance(value, collections.MutableMapping):
                self.to_env(data=value, parent_key=key)

            elif isinstance(value, collections.MutableSequence):
                value = ' '.join(item for item in value)
                if parent_key:
                    env['{}_{}'.format(parent_key, key).upper()] = value
                else:
                    env[key.upper()] = value
            else:
                if parent_key:
                    env['{}_{}'.format(parent_key, key).upper()] = str(value)
                else:
                    env[key.upper()] = str(value)

