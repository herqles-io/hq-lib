#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.base_config import BaseConfig
from hqlib.config.error import HerqlesConfigError
from hqlib.config.path_config import PathConfig

from tests.shared_data import VALID_YAML


class TestPathConfig(TestCase):

    def test_loading_from_base_config(self):
        """ Config data loads and validates """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config = BaseConfig(base_config_data)

            base_config.validate()

            path_config = PathConfig(base_config.paths)

            path_config.validate()

    def test_loading_from_dict(self):
        """ Config data loads and validates """

        path_config_data = {
            'logs': '/var/log/herqles',
            'pid': '/var/run/herqles/hq-manager.pid',
        }

        path_config = PathConfig(path_config_data)

        self.assertEqual(path_config.logs, path_config_data['logs'])

    def test_model_conversion_error(self):
        """ Config data loads and validates """

        path_config_data = 'Not a legit config'

        with self.assertRaises(HerqlesConfigError) as hce:

            PathConfig(path_config_data)

        self.assertTrue(str(hce.exception).startswith('Could not create path config: '))

    def test_dict_missing_values(self):
        """ Config data loads and validates """

        path_config_data = {
            'pid': '/var/run/herqles/hq-manager.pid',
        }

        path_config = PathConfig(path_config_data)

        with self.assertRaises(HerqlesConfigError) as hce:
            path_config.validate()

        self.assertTrue(str(hce.exception).startswith('Could not validate path config: '))


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestPathConfig))
