#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.base_config import BaseConfig
from hqlib.config.error import HerqlesConfigError
from hqlib.config.ldap_config import LDAPConfig

from tests.shared_data import VALID_YAML


class TestLDAPConfig(TestCase):

    def test_loading_from_base_config(self):
        """ Config data loads and validates """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config = BaseConfig(base_config_data)

            base_config.validate()

            ldap_config = LDAPConfig(base_config.ldap)

            ldap_config.validate()

    def test_missing_field_loading_from_base_config(self):
        """ Config data loads and validates """

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config_data['ldap'].pop('host')

            base_config = BaseConfig(base_config_data)

        with self.assertRaises(HerqlesConfigError) as hce:

            base_config.validate()

        self.assertTrue(str(hce.exception).startswith('Could not validate LDAP config: '))

    def test_loading_from_dict(self):
        """ Config data loads and validates """

        ldap_config_data = {
            'host': 'localhost',
            'domain': 'local',
            'base_dn': 'DC=test,DC=local',
            'bind_username': 'admin',
            'bind_password': 'admin_test_pwd',
        }

        ldap_config = LDAPConfig(ldap_config_data)

        self.assertEqual(ldap_config.host, ldap_config_data['host'])

    def test_model_conversion_error(self):
        """ Config data loads and validates """

        ldap_config_data = 'Not a legit config'

        with self.assertRaises(HerqlesConfigError) as hce:

            LDAPConfig(ldap_config_data)

        self.assertTrue(str(hce.exception).startswith('Could not create LDAP config: '))

    def test_dict_missing_values(self):
        """ Config data loads and validates """

        ldap_config_data = {
            'host': 'localhost',
            'domain': 'local',
            'base_dn': 'DC=test,DC=local',
            'bind_password': 'admin_test_pwd',
        }

        ldap_config = LDAPConfig(ldap_config_data)

        with self.assertRaises(HerqlesConfigError) as hce:
            ldap_config.validate()

        self.assertTrue(str(hce.exception).startswith('Could not validate LDAP config: '))


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestLDAPConfig))
