#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml

from hqlib.config import parse_config
from hqlib.config.error import HerqlesConfigError
from hqlib.config.ldap_config import LDAPConfig
from hqlib.config.path_config import PathConfig
from hqlib.config.rabbitmq_config import RabbitMQConfig
from hqlib.config.sql_config import SQLConfig

CONFIG_SECTIONS = {
    'rabbitmq': RabbitMQConfig,
    'ldap': LDAPConfig,
    'sql': SQLConfig,
    'paths': PathConfig,
}


class BaseConfig(object):
    """ Validation for Herqles framwork configuration

    Builds a collection of configuration objects as available in the data
    provided during initialization

    """

    config_data = None

    def __init__(self, config_data):
        """ Init using the config_data """

        self.config_data = config_data

        for section_key in CONFIG_SECTIONS:
            if section_key in config_data:
                config = CONFIG_SECTIONS[section_key](config_data[section_key])
                setattr(self, section_key, config)

    @property
    def rabbitmq(self):
        if not hasattr(self, '_rabbitmq'):
            raise HerqlesConfigError('RabbitMQ configuration missing')

        return self._rabbitmq

    @rabbitmq.setter
    def rabbitmq(self, value):
        self._rabbitmq = value

    @property
    def ldap(self):
        if not hasattr(self, '_ldap'):
            raise HerqlesConfigError('LDAP configuration missing')

        return self._ldap

    @ldap.setter
    def ldap(self, value):
        self._ldap = value

    @property
    def sql(self):
        if not hasattr(self, '_sql'):
            raise HerqlesConfigError('SQL configuration missing')

        return self._sql

    @sql.setter
    def sql(self, value):
        self._sql = value

    @property
    def paths(self):
        if not hasattr(self, '_paths'):
            raise HerqlesConfigError('Path configuration missing')

        return self._paths

    @paths.setter
    def paths(self, value):
        self._paths = value

    def validate(self):
        """ Validate and throw more succinct error """

        for sub_config in CONFIG_SECTIONS:
            if hasattr(self, sub_config):
                getattr(self, sub_config).validate()

def base_config_from_file(config_filename):
    """ Generate base_config from yml filename """

    base_config = BaseConfig(parse_config(config_filename))
    base_config.validate()

    return base_config


def generate_default_config_file(filename='config.yml', config_directory='./'):
    """Create a properly structured config file

    Generate a basic config yaml file with default values filled in

    """

    test_data = {
        'rabbitmq': {
            'hosts': ['localhost:5672', 'testhost:5672'],
            'username': 'herqles',
            'virtual_host': 'herqles',
        },
        'sql': {
            'driver': 'postgres',
            'host': 'localhost',
            'port': 5432,
            'database': 'herqles',
            'username': 'herqles',
            'password': 'herqles',
            'pool_size': 20,
        },
        'ldap': {
            'host': 'localhost',
            'domain': 'local',
            'base_dn': 'DC=test,DC=local',
            'bind_username': 'admin',
            'bind_password': 'admin_test_pwd',
        },
        'paths': {
            'logs': '/var/log/herqles',
            'pid': '/var/run/herqles/hq-manager.pid'
        }
    }

    with open(config_directory + filename, 'w') as config_file:
        yaml.dump(test_data, config_file, default_flow_style=False)

if __name__ == '__main__':
    generate_default_config_file()
