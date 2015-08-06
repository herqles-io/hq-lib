from enum import Enum


class ExchangeType(Enum):
    DIRECT = 'direct'
    TOPIC = 'topic'
    HEADERS = 'headers'
    FANOUT = 'fanout'
