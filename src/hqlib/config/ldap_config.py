#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from schematics.models import Model
from schematics.types import StringType
from schematics.exceptions import ModelValidationError, ModelConversionError

from hqlib.config.error import HerqlesConfigError

class LDAPConfig(Model):
    """ LDAP configs for Herqles """

    host = StringType(required=True)
    domain = StringType(required=True)
    base_dn = StringType(required=True)
    bind_username = StringType(required=True)
    bind_password = StringType(required=True)

    def __init__(self, sql_configs):
        """ Init using the base_config and raise HQ error if failures """

        try:
            super(LDAPConfig, self).__init__(sql_configs)

        except ModelConversionError, init_error:
            msg_fmt = 'Could not create LDAP config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(init_error.message)))

    def validate(self):
        """ Validate and throw more succinct error """

        try:
            super(LDAPConfig, self).validate()

        except ModelValidationError, val_error:
            msg_fmt = 'Could not validate LDAP config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(val_error.message)))
