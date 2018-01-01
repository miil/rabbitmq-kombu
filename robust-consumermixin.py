from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
import settings as s
rabbit_url = s.RABBIT_URL

# ConsumerProducerMixin
class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        print('Got message: {0}'.format(body))
        message.ack()


exchange = Exchange(s.EXCHANGE_NAME, type=s.EXCHANGE_TYPE)
queues = [Queue(s.Q_NAME, exchange, routing_key="BOB")]

with Connection(rabbit_url, heartbeat=4) as conn:
    try:
        worker = Worker(conn, queues)
        worker.run()
    except Exception as e:
        print 'error: connection problem, ', e
        raise
