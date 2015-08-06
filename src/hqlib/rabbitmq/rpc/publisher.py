from hqlib.rabbitmq.rpc.subscriber import RPCSubscriber
from hqlib.rabbitmq.routing import Publisher as RoutingPublisher
import logging
from threading import Event, _Event
import json
from pika.spec import BasicProperties
import uuid
from pika.exceptions import ChannelClosed

rpc_subscriber = None

class RPCPublisher(object):

    def __init__(self, rabbitmq, exchange_name, routingkey):
        self.logger = logging.getLogger("hq.warehouse.rabbitmq.rpc.publisher")
        self.publisher = RoutingPublisher(rabbitmq, exchange_name, routingkey)
        global rpc_subscriber
        if rpc_subscriber is None:
            rpc_subscriber = RPCSubscriber(rabbitmq)
            rpc_subscriber.start()

    def publish(self, dict):
        global rpc_subscriber
        while rpc_subscriber.consumer_tag is None:
            continue

        props = BasicProperties()
        props.reply_to = rpc_subscriber.queue_name
        props.correlation_id = str(uuid.uuid4())

        try:
            rpc_subscriber.rpc_data[props.correlation_id] = Event()
            self.publisher.publish(dict, props)
        except:
            self.logger.exception("Error publishing rpc message")
            del rpc_subscriber.rpc_data[props.correlation_id]
            props.correlation_id = None
        self.publisher.close()

        return props.correlation_id

    def get_data(self, correlation_id, wait=5, force=False):
        global rpc_subscriber

        if correlation_id in rpc_subscriber.rpc_data:
            if isinstance(rpc_subscriber.rpc_data[correlation_id], _Event):
                if force:  # Already waited and data did not show up
                    del rpc_subscriber.rpc_data[correlation_id]
                    return None

                try:
                    rpc_subscriber.rpc_data[correlation_id].wait(wait)
                except KeyboardInterrupt:
                    return None
                return self.get_data(correlation_id, force=True)
            else:
                data = rpc_subscriber.rpc_data[correlation_id]
                del rpc_subscriber.rpc_data[correlation_id]
                return data

        return None


class RPCReplyPublisher(object):

    def __init__(self, rabbitmq, queue_name, correlation_id):
        self.queue_name = queue_name
        self.correlation_id = correlation_id
        self.connection = rabbitmq.syncconnection()
        self.channel = self.connection.channel()
        self.logger = logging.getLogger("hq.warehouse.rabbitmq.rpc.publisher.reply")
        self.publishersetup()

    def publishersetup(self):
        self.logger.debug('Publisher connection to Queue ' + self.queue_name)
        try:
            self.channel.queue_declare(queue=self.queue_name, passive=True)
        except ChannelClosed:
            self.logger.warning("The rpc queue "+self.queue_name+" does not exist")

    def publish(self, dict):
        props = BasicProperties()
        props.correlation_id = self.correlation_id
        if self.channel.is_open:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name,
                                       properties=props, body=json.dumps(dict))

    def close(self):
        self.logger.debug("Publisher closing connection to Queue " + self.queue_name)
        if self.channel.is_open:
            self.channel.close()
        self.connection.close()
