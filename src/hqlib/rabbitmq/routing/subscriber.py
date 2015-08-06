import threading
from abc import ABCMeta, abstractmethod
from hqlib.rabbitmq import ExchangeType
import logging
from pika.exceptions import AMQPConnectionError


class Subscriber(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, rabbitmq, exchange_name, routing_key, queue_name="", qos=0, auto_delete=True):
        super(Subscriber, self).__init__()
        self.rabbitmq = rabbitmq
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.connection = None
        self.queue_name = queue_name
        self.qos = qos
        self.channel = None
        self.stopped = False
        self.consumer_tag = None
        self.auto_delete = auto_delete
        self.logger = logging.getLogger("hq.warehouse.rabbitmq.routing.subscriber")

    def run(self):
        reconnect = False
        while not self.stopped:
            if self.connection is not None:
                self.logger.debug("Restarting IO Loop")
                if not self.connection.is_closed and not self.connection.is_closing:
                    self.connection.close()
            try:
                if self.connection is None:
                    reconnect = True

                self.connection = self.connect(reconnect)
                reconnect = False
            except AMQPConnectionError as e:
                self.logger.error("Rabbitmq Connection error " + e.message)
                reconnect = True
                try:
                    threading.Event().wait(5)
                except KeyboardInterrupt:
                    pass
                continue
            if self.consumer_tag is not None:
                self.consumer_tag = None
            if self.queue_name.startswith("amq."):
                self.queue_name = ""
            self.connection.ioloop.start()

        if not self.connection.is_closed and not self.connection.is_closing:
            try:
                self.connection.close()
            except IOError:
                pass

    def connect(self, reconnect=False):
        self.logger.debug("Creating connection")
        connection = self.rabbitmq.asyncconnection(self.on_connection_open, reconnect)
        connection.add_on_open_error_callback(self.on_connection_open_error)
        self.logger.debug("Connection created")
        return connection

    def reconnect(self):
        self.logger.info("Subscriber reconnecting to rabbitmq")
        self.connection.ioloop.stop()

    def on_connection_open(self, connection):
        connection.add_on_close_callback(self.on_connection_closed)
        self.open_channel()

    def on_connection_open_error(self, connection, error):
        self.logger.info("RabbitMQ Connection couldn't open. Trying another server")
        connection.add_timeout(5, self.reconnect)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self.channel = None
        if self.stopped:
            self.logger.info("Connection "+str(connection)+" was closed: ("+str(reply_code)+") "+reply_text+" exchange "+self.exchange_name+" routing "+self.routing_key)
        else:
            self.logger.info("RabbitMQ Connection Closed. Reconnecting in 5 seconds (%s) %s", reply_code, reply_text)
            connection.add_timeout(5, self.reconnect)

    def open_channel(self):
        self.connection.channel(on_open_callback=self.on_channel_open)

    def close_channel(self):
        if self.channel.is_open:
            self.channel.close()

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        if self.qos != 0:
            self.channel.basic_qos(self.on_qos, prefetch_count=self.qos)
        else:
            self.setup_exchange()

    def on_qos(self, frame):
        self.setup_exchange()

    def on_channel_closed(self, channel, reply_code, reply_text):
        self.logger.info("Channel "+str(channel)+" was closed: ("+str(reply_code)+") "+reply_text+" exchange "+self.exchange_name+" routing "+self.routing_key)
        #self.connection.close()

    def setup_exchange(self):
        self.logger.debug("Subscriber Declaring Routing Exchange " + self.exchange_name)
        self.channel.exchange_declare(callback=self.on_exchange_declareok, exchange=self.exchange_name,
                                      exchange_type=ExchangeType.DIRECT.value)

    def on_exchange_declareok(self, frame):
        self.setup_queue()

    def setup_queue(self):
        self.channel.queue_declare(callback=self.on_queue_declareok, queue=self.queue_name, auto_delete=self.auto_delete)

    def on_queue_declareok(self, frame):
        if self.queue_name == "":
            self.queue_name = frame.method.queue
        if self.routing_key == "":
            self.routing_key = self.queue_name
        self.channel.queue_bind(callback=self.on_bindok, queue=self.queue_name, exchange=self.exchange_name, routing_key=self.routing_key)
        
    def on_bindok(self, frame):
        self.start_consuming()
        
    def start_consuming(self):
        self.logger.info("Starting Consume on routing exchange " + self.exchange_name+" routing "+self.routing_key)
        self.add_on_cancel_callback()
        self.consumer_tag = self.channel.basic_consume(self.on_message, self.queue_name,
                                                       arguments={"x-cancel-on-ha-failover": True})
        
    def add_on_cancel_callback(self):
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)
        
    def on_consumer_cancelled(self, frame):
        self.logger.info("Consumer was cancelled remotely. Shutting down: %r", frame)
        if not self.stopped:
            self.start_consuming()
            return
        if self.channel:
            self.stop()
            
    def on_message(self, channel, basic_deliver, properties, body):
        try:
            self.message_deliver(channel, basic_deliver, properties, body)
        except:
            self.logger.exception("Routing Subscriber threw a error on consume")
            channel.basic_nack(basic_deliver.delivery_tag, requeue=True)

    @abstractmethod
    def message_deliver(self, channel, basic_deliver, properties, body):
        pass
        
    def stop(self):
        self.logger.info("Stopping Consumer ("+str(self)+") on Routing Exchange " + self.exchange_name+" routing "+self.routing_key)
        self.stopped = True
        self.connection.ioloop.stop()
        self.rabbitmq.remove_subscriber(self)
        
    def start(self):
        self.rabbitmq.add_subscriber(self)
        self.logger.debug("Adding Consumer "+str(self))
        super(Subscriber, self).start()
