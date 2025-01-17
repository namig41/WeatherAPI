from dataclasses import dataclass

import aio_pika
import orjson

from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.message import Message


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        rq_message = self.build_message(message)
        await self._publish_message(rq_message, routing_key, exchange_name)

    async def declare_exchange(self, exchange_name: str) -> None:
        await self.channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)

    @staticmethod
    def build_message(message: Message) -> aio_pika.Message:
        return aio_pika.Message(
            body=orjson.dumps(
                {"message_type": message.message_type, "data": message.data},
            ),
            message_id=str(message.id),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            headers={},
        )

    async def _publish_message(
        self,
        rq_message: aio_pika.Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        exchange = await self._get_exchange(exchange_name)
        await exchange.publish(rq_message, routing_key=routing_key)

    async def _get_exchange(self, exchange_name: str) -> aio_pika.abc.AbstractExchange:
        return await self.channel.get_exchange(exchange_name, ensure=False)
