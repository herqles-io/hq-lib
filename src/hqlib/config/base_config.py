#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from schematics.models import Model
from schematics.types import BaseType
from schematics.types.compound import DictType
from schematics.exceptions import ModelValidationError, ModelConversionError

from hqlib.config.error import HerqlesConfigError

class BaseConfig(Model):
    """ Validation for Herqles framwork configuration """

    rabbitmq = DictType(BaseType(), required=True)
    sql = DictType(BaseType(), required=True)
    ldap = DictType(BaseType(), default=None)
    identity = DictType(BaseType(), required=True)
    assignment = DictType(BaseType(), required=True)
    paths = DictType(BaseType(), required=True)

    def __init__(self, base_config):
        """ Init using the base_config and raise HQ error if failures """

        try:
            super(BaseConfig, self).__init__(base_config)

        except ModelConversionError, init_error:
            msg_fmt = 'Could not create base config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(init_error.message)))

    def validate(self):
        """ Validate and throw more succinct error """

        try:
            super(BaseConfig, self).validate()

        except ModelValidationError, val_error:
            msg_fmt = 'Could not validate base config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(val_error.message)))
