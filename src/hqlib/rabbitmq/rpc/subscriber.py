from hqlib.rabbitmq.queue.subscriber import Subscriber as QueueSubscriber
import logging
import threading
import json
import uuid


class RPCSubscriber(QueueSubscriber):

    def __init__(self, rabbitmq):
        super(RPCSubscriber, self).__init__(rabbitmq, queue_name="rpc."+str(uuid.uuid4()))
        self.logger = logging.getLogger("hq.warehouse.rabbitmq.rpc.subscriber")
        self.rpc_data = {}

    def message_deliver(self, channel, basic_deliver, properties, body):
        if properties.correlation_id in self.rpc_data:
            if isinstance(self.rpc_data[properties.correlation_id], threading._Event):
                event = self.rpc_data[properties.correlation_id]
                self.rpc_data[properties.correlation_id] = json.loads(body)
                event.set()
            else:
                self.logger.warning("Duplicate rpc correlation_id " + properties.correlation_id)
        else:
            self.logger.warning("Unknown rpc correlation_id " + properties.correlation_id + "with data " + body)

        channel.basic_ack(basic_deliver.delivery_tag)
