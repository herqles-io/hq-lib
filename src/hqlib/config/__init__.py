#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from yaml import YAMLError

from hqlib.config.error import HerqlesConfigError

def parse_config(config_path):
    try:
        with open(config_path, 'r') as yaml_file:
            config = yaml.load(yaml_file)
        return config

    except YAMLError as yaml_error:
        raise HerqlesConfigError('Could not parse config file: ' + str(yaml_error))

    except IOError as io_error:
        raise HerqlesConfigError('Could not load config file: ' + str(io_error))
