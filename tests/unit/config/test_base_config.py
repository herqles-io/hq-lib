#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.base_config import BaseConfig
from hqlib.config.error import HerqlesConfigError


VALID_YAML = """---
  rabbitmq:
    hosts:
      - "localhost:5672"
      - "testhost:5672"
    username: herqles
    password: herqles
    virtual_host: herqles
  sql:
    driver: postgres
    host: localhost
    port: 5432
    database: herqles
    username: herqles
    password: herqles
    pool_size: "20"
  identity:
    driver: hqmanager.identity.ldap_driver
  assignment:
    mapping:
      "CN=sys_linuxadmins,OU=System Access,OU=Administrative Groups":
        - "herqles.*"
      "CN=Autobahn,OU=Administrative Groups":
        - herqles.task.get
        - herqles.framework.cd_stage.create
        - herqles.framework.cd_stage.get
        - herqles.framework.cd_deploy.create
        - herqles.framework.cd_deploy.get
        - herqles.framework.cd_rollback.create
        - herqles.framework.cd_rollback.get
    driver: hqmanager.assignment.ldap_driver
  paths:
    logs: /var/log/herqles
    pid: /var/run/herqles/hq-manager.pid
  ldap:
    host: localhost
    domain: local
    base_dn: "DC=test,DC=local"
    bind_username: admin
    bind_password: "admin_test_pwd" """

INCOMPLETE_YAML = """---
  rabbitmq:
    hosts:
      - "localhost:5672"
      - "testhost:5672"
    username: herqles
    password: herqles
    virtual_host: herqles """

class TestBaseConfig(TestCase):

    def test_base_config_loading(self):
    
        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            base_config_data = parse_config(temp_config_file.name)

            base_config = BaseConfig(base_config_data)

            base_config.validate()

    def test_base_config_data(self):
    
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

    def test_incomplete_base_config_data(self):
    
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
