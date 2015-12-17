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

            self.assertEqual(correct_paths_data, base_config.paths)

            incorrect_paths_data = {
                'logs': '/something/very/very/wrong',
                'pid': '/var/run/herqles/hq-manager.pid'
            }

            self.assertNotEqual(incorrect_paths_data, base_config.paths)

    def test_incomplete_config_data(self):
        """ Incomplete config data raises HerqlesConfigError """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(INCOMPLETE_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            with self.assertRaises(HerqlesConfigError) as hce:
                base_config = BaseConfig(base_config_data)

                base_config.validate()

            self.assertTrue(str(hce.exception).startswith('Could not validate base config: '))


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestBaseConfig))
