#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

INCOMPLETE_YAML = """---
  rabbitmq:
    hosts:
      - "localhost:5672"
      - "testhost:5672"
    username: herqles
    password: herqles
    virtual_host: herqles """