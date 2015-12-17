#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.base_config import BaseConfig
from hqlib.config.error import HerqlesConfigError
from hqlib.config.sql_config import SQLConfig

from tests.shared_data import VALID_YAML


class TestSQLConfig(TestCase):

    def test_loading_from_base_config(self):
        """ Config data loads and validates """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config = BaseConfig(base_config_data)

            base_config.validate()

            sql_config = SQLConfig(base_config.sql)

            sql_config.validate()

    def test_loading_from_dict(self):
        """ Config data loads and validates """

        sql_config_data = {
            "driver": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "herqles",
            "username": "herqles",
            "password": "herqles",
            "pool_size": "20",
        }

        sql_config = SQLConfig(sql_config_data)

        self.assertEqual(sql_config.driver, sql_config_data['driver'])

    def test_model_conversion_error(self):
        """ Config data loads and validates """

        sql_config_data = 'Not a legit config'

        with self.assertRaises(HerqlesConfigError) as hce:

            SQLConfig(sql_config_data)

        self.assertTrue(str(hce.exception).startswith('Could not create SQL config: '))

    def test_dict_missing_values(self):
        """ Config data loads and validates """

        sql_config_data = {
            "driver": "postgres",
            "host": "localhost",
            "port": "5432",
            "username": "herqles",
            "password": "herqles",
            "pool_size": "20",
        }

        sql_config = SQLConfig(sql_config_data)

        with self.assertRaises(HerqlesConfigError) as hce:
            sql_config.validate()

        self.assertTrue(str(hce.exception).startswith('Could not validate SQL config: '))


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestSQLConfig))
