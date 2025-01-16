from functools import lru_cache

from faststream.rabbit import RabbitBroker

from infrastructure.message_broker.config import EventBusConfig


@lru_cache(1)
def init_message_broker(event_bus_config: EventBusConfig) -> RabbitBroker:
    broker: RabbitBroker = RabbitBroker(url=event_bus_config.get_url)
    return broker
