from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.constants import (
    USER_EXCHANGE_NAME,
    USER_QUEUE_NAME,
    USER_ROUTE_KEY_TEMPLATE,
    WEATHER_EXCHANGE_NAME,
    WEATHER_QUEUE_NAME,
    WEATHER_ROUTE_KEY_TEMPLATE,
)


async def configure_message_broker(message_broker: BaseMessageBroker) -> None:
    await message_broker.declare_exchange(USER_EXCHANGE_NAME)
    await message_broker.declare_queue(
        USER_QUEUE_NAME,
        USER_EXCHANGE_NAME,
        USER_ROUTE_KEY_TEMPLATE,
    )

    await message_broker.declare_exchange(WEATHER_EXCHANGE_NAME)
    await message_broker.declare_queue(
        WEATHER_QUEUE_NAME,
        WEATHER_EXCHANGE_NAME,
        WEATHER_ROUTE_KEY_TEMPLATE,
    )
