#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ListType
from schematics.exceptions import ModelValidationError, ModelConversionError

from hqlib.config.error import HerqlesConfigError

class RabbitMQConfig(Model):
    """ RabbitMQ configurations for Herqles """

    hosts = ListType(StringType(), required=True, min_size=1)
    username = StringType(required=True)
    password = StringType(required=True)
    virtual_host = StringType(default='/')

    def __init__(self, rabbitmq_configs):
        """ Init using the base_config and raise HQ error if failures """

        try:
            super(RabbitMQConfig, self).__init__(rabbitmq_configs)

        except ModelConversionError, init_error:
            msg_fmt = 'Could not create rabbitmq config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(init_error.message)))

    def validate(self):
        """ Validate and throw more succinct error """

        try:
            super(RabbitMQConfig, self).validate()

        except ModelValidationError, val_error:
            msg_fmt = 'Could not validate rabbitmq config: {}'
            raise HerqlesConfigError(msg_fmt.format(json.dumps(val_error.message)))
