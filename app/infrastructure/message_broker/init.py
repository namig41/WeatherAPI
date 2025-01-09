from dataclasses import dataclass

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from .config import EventBusConfig


@dataclass
class ConnectionFactory:
    config: EventBusConfig

    async def get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(
            host=self.config.host,
            port=self.config.port,
            login=self.config.login,
            password=self.config.password,
        )


@dataclass
class ChannelFactory:
    rq_connection_pool: Pool[aio_pika.abc.AbstractConnection]

    async def get_channel(self) -> aio_pika.abc.AbstractChannel:
        async with self.rq_connection_pool.acquire() as connection:
            return await connection.channel(publisher_confirms=False)
