from kombu import Connection, Exchange, Queue, Producer
import time
import settings as s

rabbit_url = s.RABBIT_URL

conn = Connection(rabbit_url)

channel = conn.channel()

exchange = Exchange(s.EXCHANGE_NAME, type=s.EXCHANGE_TYPE)

producer = Producer(exchange=exchange, channel=channel, routing_key=s.routing_key)

queue = Queue(name=s.Q_NAME, exchange=exchange, routing_key=s.routing_key)
queue.maybe_bind(conn)
queue.declare()

producer.publish("===>>> " + time.strftime("%Y-%m-%d %H:%M:%S") )
