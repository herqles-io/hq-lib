#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.base_config import BaseConfig
from hqlib.config.error import HerqlesConfigError
from hqlib.config.rabbitmq_config import RabbitMQConfig

from tests.shared_data import VALID_YAML


class TestRabbitMQConfig(TestCase):

    def test_loading_from_base_config(self):
        """ Config data loads and validates """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config = BaseConfig(base_config_data)

            base_config.validate()

            rabbitmq_config = RabbitMQConfig(base_config.rabbitmq)

            rabbitmq_config.validate()

    def test_loading_from_dict(self):
        """ Config data loads and validates """

        rabbitmq_config_data = {
            'hosts': ['localhost:5672', 'testhost:5672'],
            'username': 'herqles',
            'password': 'herqles',
            'virtual_host': 'herqles',
        }

        rabbitmq_config = RabbitMQConfig(rabbitmq_config_data)

        self.assertEqual(rabbitmq_config.username, rabbitmq_config_data['username'])

    def test_model_conversion_error(self):
        """ Config data loads and validates """

        rabbitmq_config_data = 'Not a legit config'

        with self.assertRaises(HerqlesConfigError) as hce:

            RabbitMQConfig(rabbitmq_config_data)

        self.assertTrue(str(hce.exception).startswith('Could not create rabbitmq config: '))

    def test_dict_missing_values(self):
        """ Config data loads and validates """

        rabbitmq_config_data = {
            'hosts': ['localhost:5672', 'testhost:5672'],
            'username': 'herqles',
            'virtual_host': 'herqles',
        }


        rabbitmq_config = RabbitMQConfig(rabbitmq_config_data)

        with self.assertRaises(HerqlesConfigError) as hce:
            rabbitmq_config.validate()

        self.assertTrue(str(hce.exception).startswith('Could not validate rabbitmq config: '))


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestRabbitMQConfig))
