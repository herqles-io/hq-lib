import pika
from hqlib.rabbitmq.exchangetype import ExchangeType
from pika.adapters.select_connection import SelectPoller

SelectPoller.TIMEOUT = 0.01


class RabbitMQ(object):

    def __init__(self, hosts, username, password, virtualhost):
        self.hosts = hosts
        self.username = username
        self.password = password
        self.virtualhost = virtualhost
        self.connectionParams = []
        self.paramIndex = 0
        self.active_subscribers = []
        self.active_publishers = []

    def setup_database(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        for host in self.hosts:
            self.connectionParams.append(pika.ConnectionParameters(host=host[0], port=host[1],
                                                                   virtual_host=self.virtualhost,
                                                                   credentials=credentials))
        self.paramIndex = 0

    def add_publisher(self, publisher):
        self.active_publishers.append(publisher)

    def remove_publisher(self, publisher):
        self.active_publishers.remove(publisher)

    def add_subscriber(self, subscriber):
        self.active_subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.active_subscribers.remove(subscriber)

    def syncconnection(self, reconnect=False):
        if reconnect:
            self.paramIndex += 1
            if self.paramIndex >= len(self.connectionParams):
                self.paramIndex = 0
        return pika.BlockingConnection(parameters=self.connectionParams[self.paramIndex])

    def asyncconnection(self, callback, reconnect=False):
        if reconnect:
            self.paramIndex += 1
            if self.paramIndex >= len(self.connectionParams):
                self.paramIndex = 0
        connection = pika.SelectConnection(parameters=self.connectionParams[self.paramIndex],
                                           on_open_callback=callback, stop_ioloop_on_close=False)
        return connection