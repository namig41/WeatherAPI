import asyncio

import pytest
from aio_pika.abc import AbstractRobustConnection
from punq import Container

from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.message import Message
from infrastructure.message_broker.message_broker import RabbitMQMessageBroker
from infrastructure.message_broker.message_broker_factory import (
    ConnectionFactory,
    MessageBrokerFactory,
)


@pytest.mark.asyncio
async def test_message_broker(container: Container):
    connection_factory: ConnectionFactory = container.resolve(ConnectionFactory)
    connection: AbstractRobustConnection = await connection_factory.get_connection()

    async with connection:
        channel = await connection.channel()

        message_broker: BaseMessageBroker = RabbitMQMessageBroker(channel=channel)

        # Объявляем обменник
        exchange_name = "test_exchange"
        await message_broker.declare_exchange(exchange_name)

        message_broker.declare_queue("my_queue", exchange_name, "test.*")

        message = Message(message_type="example", data={"key": "value"})
        routing_key = "test.key"
        for _ in range(10):
            await message_broker.publish_message(message, routing_key, exchange_name)
            await asyncio.sleep(5)


@pytest.mark.asyncio
async def test_message_broker_with_factory(container: Container):
    connection_factory: MessageBrokerFactory = container.resolve(MessageBrokerFactory)
    message_broker: BaseMessageBroker = await connection_factory.get_message_broker()

    # Объявляем обменник
    exchange_name: str = "test_exchange"
    await message_broker.declare_exchange(exchange_name)

    message_broker.declare_queue("my_queue", exchange_name, "test.*")

    # Публикуем сообщение
    message = Message(message_type="example", data={"key": "value"})
    routing_key: str = "test.key"
    for _ in range(10):
        await message_broker.publish_message(message, routing_key, exchange_name)
        await asyncio.sleep(1)

    message_broker.close()
