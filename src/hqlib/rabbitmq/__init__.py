#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
from pika.adapters.select_connection import SelectPoller

from hqlib.rabbitmq.exchangetype import ExchangeType

SelectPoller.TIMEOUT = 0.01


class RabbitMQ(object):

    def __init__(self, rabbitmq_config):

        self.hosts = []
        for host in rabbitmq_config.hosts:
            (ip, port) = host.split(":")
            self.hosts.append((ip, int(port)))

        self.username = rabbitmq_config.username
        self.password = rabbitmq_config.password
        self.virtualhost = rabbitmq_config.virtualhost
        self.connection_params = []
        self.param_index = 0
        self.active_subscribers = []
        self.active_publishers = []

    def setup_database(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        for host in self.hosts:
            self.connection_params.append(pika.ConnectionParameters(host=host[0], port=host[1],
                                                                   virtual_host=self.virtualhost,
                                                                   credentials=credentials))
        self.param_index = 0

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
            self.param_index += 1
            if self.param_index >= len(self.connection_params):
                self.param_index = 0
        return pika.BlockingConnection(parameters=self.connection_params[self.param_index])

    def asyncconnection(self, callback, reconnect=False):
        if reconnect:
            self.param_index += 1
            if self.param_index >= len(self.connection_params):
                self.param_index = 0
        connection = pika.SelectConnection(parameters=self.connection_params[self.param_index],
                                           on_open_callback=callback, stop_ioloop_on_close=False)
        return connection
