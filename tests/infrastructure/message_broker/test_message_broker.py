import pytest
from punq import Container

from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.message import Message
from infrastructure.message_broker.message_broker_factory import ChannelFactory


@pytest.mark.asyncio
async def test_message_broker(container: Container):
    channel_factory = ChannelFactory()
    channel = channel_factory.get_channel()

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    message_broker.set_channel(channel)

    # Объявляем обменник
    exchange_name = "test_exchange"
    await message_broker.declare_exchange(exchange_name)

    # Публикуем сообщение
    message = Message(message_type="example", data={"key": "value"})
    routing_key = "test.key"
    await message_broker.publish_message(message, routing_key, exchange_name)
