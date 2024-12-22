from celery import Celery
from infrastructure.cache.config import CacheConfig
from punq import Container

from application.di.container import init_container


def create_task_queue(cache_config: CacheConfig) -> Celery:
    task_queue: Celery = Celery(
        broker=cache_config.get_url("redis"),
        backend=cache_config.get_url("redis"),
    )
    return task_queue


if __name__ == "__main__":
    container: Container = init_container()
    cache_config: CacheConfig = container.resolve(CacheConfig)
    app: Celery = create_task_queue(cache_config)
