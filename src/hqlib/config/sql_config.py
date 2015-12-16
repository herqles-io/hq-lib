#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.exceptions import ModelValidationError, ModelConversionError

from hqlib.config.error import HerqlesConfigError

class SQLConfig(Model):
    """ SQL configs for Herqles """

    driver = StringType(required=True)
    host = StringType(required=True)
    port = IntType(required=True)
    database = StringType(required=True)
    username = StringType(required=True)
    password = StringType(required=True)
    pool_size = IntType(default=20)

    def __init__(self, sql_configs):
        """ Init using the base_config and raise HQ error if failures """

        try:
            super(SQLConfig, self).__init__(sql_configs)

        except ModelConversionError, init_error:
            msg_fmt = 'Could not create SQL config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(init_error.message)))

    def validate(self):
        """ Validate and throw more succinct error """

        try:
            super(SQLConfig, self).validate()

        except ModelValidationError, val_error:
            msg_fmt = 'Could not validate SQL config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(val_error.message)))
