import json
from hqlib.rabbitmq import ExchangeType
import logging
from pika.exceptions import AMQPConnectionError
import threading


class Publisher(object):
    
    def __init__(self, rabbitmq, exchange_name, routingkey):
        self.exchange_name = exchange_name
        self.routingkey = routingkey
        self.rabbitmq = rabbitmq
        self.connection = None
        self.channel = None
        self.logger = logging.getLogger("hq.warehouse.rabbitmq.routing.publisher")
        self.publishersetup()
        
    def publishersetup(self):

        tries = self.rabbitmq.connectionParams

        try:
            self.connection = self.rabbitmq.syncconnection()
        except AMQPConnectionError as e:
            error = e
            self.logger.error("Rabbitmq Connection error " + e.message)
            tries -= 1
            while tries > 0:
                try:
                    self.connection = self.rabbitmq.syncconnection(True)
                    error = None
                    break
                except AMQPConnectionError as e:
                    tries -= 1
                    error = e
                    self.logger.error("Rabbitmq Connection error " + e.message)

            if error is not None:
                self.logger.error("RabbitMQ routing publisher hit max reties")
                raise error

        self.channel = self.connection.channel()
        self.logger.debug('Publisher connection to Routing Exchange ' + self.exchange_name + ' ' + self.routingkey)
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=ExchangeType.DIRECT.value)
    
    def publish(self, dict, props=None):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.routingkey, properties=props,
                                   body=json.dumps(dict))
    
    def close(self):
        self.logger.debug("Publisher closing connection to Routing Exchange " + self.exchange_name)
        if self.connection is not None:
            self.channel.close()
            self.connection.close()
