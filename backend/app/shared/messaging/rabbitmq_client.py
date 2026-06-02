import json
import os
import logging
import pika

logger = logging.getLogger(__name__)

class RabbitMQClient:
    def __init__(self):
        self._url = os.getenv("RABBITMQ_URL")

    def _connect(self) -> tuple[pika.BlockingConnection, pika.channel.Channel]:
        parameters = pika.URLParameters(self._url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        return connection, channel

    def publish(self, queue: str, message: dict) -> None:
        connection, channel = self._connect()
        try:
            channel.queue_declare(queue=queue, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
            logger.info("Message published to queue '%s'", queue)
        finally:
            connection.close()

    def consume(self, queue: str, callback) -> None:
        connection, channel = self._connect()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue, on_message_callback=callback)
        logger.info("Waiting for messages on queue '%s'", queue)
        channel.start_consuming()