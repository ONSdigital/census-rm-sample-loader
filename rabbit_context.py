import os

import pika

from Exceptions import RabbitConnectionClosedError


class RabbitContext:
    def __init__(self):
        self._host = os.environ.get('RABBITMQ_SERVICE_HOST', 'localhost')
        self._port = os.environ.get('RABBITMQ_SERVICE_PORT', '5672')
        self._vhost = os.environ.get('RABBITMQ_VHOST', '/')
        self._queue = os.environ.get('RABBITMQ_QUEUE', 'localtest')
        self._exchange = os.environ.get('RABBITMQ_EXCHANGE', '')
        self._user = os.environ.get('RABBITMQ_USER', 'guest')
        self._password = os.environ.get('RABBITMQ_PASSWORD', 'guest')

    def __enter__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(self._host,
                                      self._port,
                                      self._vhost,
                                      pika.PlainCredentials(self._user, self._password)))
        self._channel = self._connection.channel()

        if self._queue == 'localtest':
            self._channel.queue_declare(queue=self._queue)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def publish_message(self, message, content_type: str):
        if not self._connection.is_open:
            raise RabbitConnectionClosedError
        self._channel.basic_publish(exchange=self._exchange,
                                    routing_key=self._queue,
                                    body=str(message),
                                    properties=pika.BasicProperties(content_type=content_type))
