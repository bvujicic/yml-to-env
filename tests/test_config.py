import os

import pytest
import yaml

from yml_config import Config


@pytest.fixture()
def data():
    return {
        'bool': False,
        'number': 1,
        'string': 'test_string',
        'sequence': ['item1', 'item2', 'item3'],
        'mapping': {
            'key1': 'value1',
            'key2': {
                'key2a': 'value2a',
                'key2b': 'value2b'
            },
            'key3': ['value3a', 'value3b', 'value3c'],
            'key4': True
        }
    }


@pytest.fixture()
def config_dict(data):
    return Config(data)


@pytest.fixture()
def config_yml(data):
    with open('config.yml', 'w') as fp:
        yaml.dump(data=data, stream=fp)

    yield Config.from_yaml(path='config.yml')

    os.remove('config.yml')


class TestConfig:

    def test_init_config(self, config_dict):
        assert 'mapping' in config_dict

    def test_init_config_yml(self, config_yml):
        assert 'mapping' in config_yml

    def test_init_config_bad_file(self):
        with pytest.raises(IOError):
            Config.from_yaml(path='badfile')

    def test_dump_to_env(self, config_yml):
        config_yml.to_env()

        assert 'BOOL' in os.environ
        assert 'SEQUENCE' in os.environ
        assert 'MAPPING_KEY1' in os.environ

    def test_retrieve_variable_success(self, config_yml):
        test_value = 'test_value'
        os.environ['TEST_KEY'] = test_value

        assert config_yml('TEST_KEY') == test_value

    def test_retrieve_variable_fail(self, config_yml):
        assert config_yml('WRONG_KEY', 'wrong_value') == 'wrong_value'

    def test_set_variable_success(self, config_yml):
        test_value = 'test_value'
        config_yml['SET_KEY'] = test_value

        assert 'SET_KEY' in os.environ
        assert os.environ['SET_KEY'] == test_value
