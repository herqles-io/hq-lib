#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

def unix_time_millis(from_datetime):
    """ Convert a datetime into milliseconds since epoch """

    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=from_datetime.tzinfo)
    epoch_delta = from_datetime - epoch
    return int(epoch_delta.total_seconds() * 1000.0)
