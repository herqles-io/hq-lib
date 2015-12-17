#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.error import HerqlesConfigError

from tests.shared_data import VALID_YAML, INVALID_YAML


class TestParseConfig(TestCase):

    def test_missing_file_error_handling(self):
        """ Missing config file should raise HerqlesConfigError """

        with self.assertRaises(HerqlesConfigError) as hce:
            parse_config('bogus_filename')

        self.assertTrue(str(hce.exception).startswith('Could not load config file: '))

    def test_parse_config_file_load(self):
        """ Valid yaml file will load """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            parse_config(temp_config_file.name)

    def test_config_file_load_failure(self):
        """ File with invalid YAML will raise HerqlesConfigError """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(INVALID_YAML)
            temp_config_file.flush()

            with self.assertRaises(HerqlesConfigError) as hce:
                parse_config(temp_config_file.name)

            self.assertTrue(str(hce.exception).startswith('Could not parse config file: '))


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestParseConfig))
