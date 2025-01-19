from faststream.rabbit import RabbitBroker

from infrastructure.message_broker.config import MessageBrokerConfig
from presentation.bot.consumers.handlers import router


async def run_consumer() -> None:
    message_broker_config: MessageBrokerConfig = MessageBrokerConfig()
    broker: RabbitBroker = RabbitBroker(
        url=message_broker_config.get_url,
    )

    broker.include_router(router=router)

    await broker.start()
