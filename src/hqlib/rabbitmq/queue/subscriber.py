import threading
from abc import ABCMeta, abstractmethod
import logging
from pika.exceptions import AMQPConnectionError


class Subscriber(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, rabbitmq, queue_name="", no_ack=False):
        super(Subscriber, self).__init__()
        self.rabbitmq = rabbitmq
        self.queue_name = queue_name
        self.no_ack = no_ack
        self.connection = None
        self.channel = None
        self.stopped = False
        self.consumer_tag = None
        self.logger = logging.getLogger("hq.warehouse.rabbitmq.queue.subscriber")

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
                self.logger.error("Anonymous Queue Subscriber cannot be restarted.")
                self.stop()
                break
            self.connection.ioloop.start()

        if not self.connection.is_closed and not self.connection.is_closing:
            try:
                self.connection.close()
            except IOError:
                pass

    def connect(self, reconnect=False):
        connection = self.rabbitmq.asyncconnection(self.on_connection_open, reconnect)
        connection.add_on_open_error_callback(self.on_connection_open_error)
        return connection

    def reconnect(self):
        self.logger.info("Subscriber reconnecting to rabbitmq")
        self.connection.ioloop.stop()

    def on_connection_open(self, connection):
        connection.add_on_close_callback(self.on_connection_closed)
        self.open_channel()

    def on_connection_open_error(self, connection, error):
        self.logger.debug("RabbitMQ Connection couldn't open. Trying another server")
        connection.add_timeout(5, self.reconnect)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self.channel = None
        if self.stopped:
            self.logger.debug("Connection "+str(connection)+" was closed: ("+str(reply_code)+") "+reply_text+" queue "+self.queue_name)
        else:
            self.logger.debug("RabbitMQ Connection Closed. Reconnecting in 5 seconds (%s) %s", reply_code, reply_text)
            connection.add_timeout(5, self.reconnect)

    def open_channel(self):
        self.connection.channel(on_open_callback=self.on_channel_open)
        
    def close_channel(self):
        if self.channel.is_open:
            self.channel.close()

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        self.setup_queue()

    def on_channel_closed(self, channel, reply_code, reply_text):
        self.logger.info("Channel "+str(channel)+" was closed: ("+str(reply_code)+") ")
        #self.connection.close()

    def setup_queue(self):
        self.logger.debug("Subscriber Declaring Queue " +self.queue_name)
        self.channel.queue_declare(callback=self.on_queue_declareok, queue=self.queue_name, auto_delete=True)

    def on_queue_declareok(self, frame):
        self.queue_name = frame.method.queue
        self.start_consuming()
        
    def start_consuming(self):
        self.logger.info("Starting Consume on Queue " + self.queue_name)
        self.add_on_cancel_callback()
        self.consumer_tag = self.channel.basic_consume(self.on_message, self.queue_name,
                                                       arguments={"x-cancel-on-ha-failover": True}, no_ack=self.no_ack)
        
    def add_on_cancel_callback(self):
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)
        
    def on_consumer_cancelled(self, frame):
        self.logger.debug("Consumer was cancelled remotely. Shutting down: %r", frame)
        if not self.stopped:
            self.start_consuming()
            return
        if self.channel:
            self.stop()
            
    def on_message(self, channel, basic_deliver, properties, body):
        try:
            self.message_deliver(channel, basic_deliver, properties, body)
        except:
            self.logger.exception("Queue Subscriber threw a error on consume")
            if self.no_ack is False:
                channel.basic_nack(basic_deliver.delivery_tag, requeue=True)

    @abstractmethod
    def message_deliver(self, channel, basic_deliver, properties, body):
        pass
        
    def stop(self):
        self.logger.info("Stopping Consumer on Queue " + self.queue_name)
        self.stopped = True
        self.connection.ioloop.stop()
        self.rabbitmq.remove_subscriber(self)
        
    def start(self):
        self.rabbitmq.add_subscriber(self)
        self.logger.debug("Adding Consumer "+str(self))
        super(Subscriber, self).start()
