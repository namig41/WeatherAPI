from infrastructure.message_broker.constants import USER_EXCHANGE_NAME
from infrastructure.message_broker.message import Message
from infrastructure.message_broker.producer.base import BaseProducer


class UserProducer(BaseProducer):
    async def publish(self, message: Message) -> None:
        await self.message_broker.publish_message(
            message,
            "user.user",
            USER_EXCHANGE_NAME,
        )
