#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
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

INVALID_YAML = """---
  rabbitmq:
    hosts
    - "localhost:5672"
    - "testhost:5672"
    username: herqles
    password: herqles
    virtual_host: herqles"""

class TestParseConfig(TestCase):

    def test_missing_file_error_handling(self):
        """ Missing config file should raise HerqlesConfigError """

        with self.assertRaises(HerqlesConfigError) as hce:
            parse_config('bogus_filename')

        self.assertTrue(str(hce.exception).startswith('Could not load config file: '))

    def test_parse_config_file_load(self):

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(VALID_YAML)
            temp_config_file.flush()

            parse_config(temp_config_file.name)

    def test_config_file_load_failure(self):

        with tempfile.NamedTemporaryFile() as temp_config_file:
            temp_config_file.write(INVALID_YAML)
            temp_config_file.flush()

            with self.assertRaises(HerqlesConfigError) as hce:
                parse_config(temp_config_file.name)

            self.assertTrue(str(hce.exception).startswith('Could not parse config file: '))


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestParseConfig))
