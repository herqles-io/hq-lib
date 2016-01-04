#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.base_config import BaseConfig
from hqlib.config.error import HerqlesConfigError

from tests.shared_data import VALID_YAML, INCOMPLETE_YAML


class TestBaseConfig(TestCase):

    def test_base_config_loading(self):
        """ Config data loads and validates """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config = BaseConfig(base_config_data)

            base_config.validate()

    def test_base_config_data(self):
        """ Proper config data loads, is present and is accurate """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config = BaseConfig(base_config_data)

            base_config.validate()

            correct_paths_data = {
                'logs': '/var/log/herqles',
                'pid': '/var/run/herqles/hq-manager.pid'
            }

            self.assertEqual(correct_paths_data['logs'], base_config.paths.logs)

            incorrect_paths_data = {
                'logs': '/something/very/very/wrong',
                'pid': '/var/run/herqles/hq-manager.pid'
            }

            self.assertNotEqual(incorrect_paths_data['logs'], base_config.paths.logs)

    def test_missing_config(self):
        """ Incomplete config data raises HerqlesConfigError """

        base_config_data = {
            'sql': {
                "driver": "postgres",
                "host": "localhost",
                "port": "5432",
                "database": "herqles",
                "username": "herqles",
                "password": "herqles",
                "pool_size": "20",
            }
        }

        with self.assertRaises(HerqlesConfigError) as hce:
            base_config = BaseConfig(base_config_data)
            sql = base_config.sql
            hosts = base_config.rabbitmq.hosts

        self.assertTrue(str(hce.exception).startswith('RabbitMQ configuration missing'))

    def test_config_validation(self):
        """ Incomplete config data raises HerqlesConfigError """

        base_config_data = {
            'rabbitmq': {
                'hosts': ['localhost:5672', 'testhost:5672'],
                'username': 'herqles',
                'virtual_host': 'herqles',
            }
        }

        with self.assertRaises(HerqlesConfigError) as hce:
            base_config = BaseConfig(base_config_data)

            base_config.validate()

        err_msg = 'Could not validate rabbitmq config: {"password": ["This field is required."]}'
        self.assertEqual(str(hce.exception), err_msg)


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestBaseConfig))
