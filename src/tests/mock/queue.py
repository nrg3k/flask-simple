import logging

class MockQueue(object):
    def __init__(self):
        self.publishes = {}

    def channel(self):
        return self

    def basic_publish(self, exchange, routing_key, body, properties):
        if not self.publishes.get(exchange):
            self.publishes[exchange] = []

        self.publishes[exchange].append(body)

    def dequeue(self, exchange):
        queue = self.publishes.get(exchange)
        logging.info("dict:{}, queue:{}, exchange:{}".format(self.publishes, queue, exchange))
        if queue:
            return queue.pop(0)

    def exchange_declare(self, *args, **kwargs):
        pass

    def queue_declare(self, *args, **kwargs):
        pass

    def queue_bind(self, *args, **kwargs):
        pass
