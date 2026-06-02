import json
import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
load_dotenv()

import pika
from app.shared.messaging.rabbitmq_client import RabbitMQClient
from app.shared.email.email_service import EmailService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

QUEUE_EMAIL_CONFIRMATION = "email.confirmation"

rabbitmq_client = RabbitMQClient()


def handle_email_confirmation(ch, method, properties, body: bytes) -> None:
    try:
        data = json.loads(body)
        to = data["to"]
        subject = data["subject"]
        html = data["html"]

        logger.info("Sending confirmation email to %s", to)
        email_service = EmailService()
        email_service.send(to=to, subject=subject, html=html)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Email sent and ack'd for %s", to)

    except Exception as exc:
        logger.error("Failed to process email message: %s", exc)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == "__main__":
    logger.info("Email worker started")
    rabbitmq_client.consume(
        queue=QUEUE_EMAIL_CONFIRMATION,
        callback=handle_email_confirmation,
    )