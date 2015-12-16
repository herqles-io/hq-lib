#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from schematics.models import Model
from schematics.types import StringType
from schematics.exceptions import ModelValidationError, ModelConversionError

from hqlib.config.error import HerqlesConfigError

class PathConfig(Model):
    """ Path configuration for Herqles """

    logs = StringType(required=True)
    pid = StringType(required=True)

    def __init__(self, path_configs):
        """ Init using the base_config and raise HQ error if failures """

        try:
            super(PathConfig, self).__init__(path_configs)

        except ModelConversionError, init_error:
            msg_fmt = 'Could not create path config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(init_error.message)))

    def validate(self):
        """ Validate and throw more succinct error """

        try:
            super(PathConfig, self).validate()

        except ModelValidationError, val_error:
            msg_fmt = 'Could not validate path config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(val_error.message)))
