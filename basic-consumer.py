from kombu import Connection, Exchange, Queue, Consumer
import settings as s


rabbit_url = s.RABBIT_URL

conn = Connection(rabbit_url)

exchange = Exchange("example-exchange", type="direct")

queue = Queue(name="example-queue", exchange=exchange, routing_key="BOB")


def process_message(body, message):
    print("The body is {}".format(body))
    message.ack()


with Consumer(conn, queues=queue, callbacks=[process_message], accept=["text/plain"]):
    conn.drain_events(timeout=2)
