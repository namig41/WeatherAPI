from infrastructure.message_broker.constants import WEATHER_EXCHANGE_NAME
from infrastructure.message_broker.message import Message
from infrastructure.message_broker.producer.base import BaseProducer


class WeatherProducer(BaseProducer):
    async def publish(self, message: Message) -> None:
        await self.message_broker.publish_message(
            message, "weather.weather", WEATHER_EXCHANGE_NAME,
        )
